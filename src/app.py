"""Bootstrap and dependency wiring for the application."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import structlog
import uvicorn

from src.core.clock import SimulationClock
from src.core.config import SimulatorConfig, load_config
from src.core.engine import SimulationEngine
from src.core.patient_pool import PatientPool
from src.core.state import SimulationState
from src.data.value_set_loader import ValueSetLoader
from src.generators.message_factory import MessageFactory
from src.workflows.workflow_registry import WorkflowRegistry
from src.workflows.step_handlers.base import init_handlers
from src.transport.message_router import MessageRouter
from src.utils.logging_config import setup_logging
from src.utils.message_log import MessageLog
from src.web.api import create_app
from src.web.dependencies import deps
from src.web.websocket import WebSocketManager

logger = structlog.get_logger(__name__)


def bootstrap(config: SimulatorConfig | None = None) -> dict[str, Any]:
    """Wire up all dependencies and return them as a dict."""
    if config is None:
        config = load_config()

    setup_logging()

    # Core
    state = SimulationState()
    clock = SimulationClock()
    message_log = MessageLog()
    ws_manager = WebSocketManager()

    # Patient pool
    patient_pool = PatientPool(
        pool_size=config.patient_pool.pool_size,
        min_age=config.patient_pool.min_age,
        max_age=config.patient_pool.max_age,
        insurance_rate=config.patient_pool.insurance_rate,
    )
    logger.info("initializing_patient_pool", size=config.patient_pool.pool_size)
    patient_pool.initialize()

    # Message factory
    message_factory = MessageFactory(config.facility, config.hl7_version)

    # Message router + destinations
    message_router = MessageRouter(message_log)
    for dest_config in config.transport.destinations:
        message_router.add_destination(dest_config)

    # Set up WebSocket broadcast
    async def ws_broadcast(data: dict[str, Any]) -> None:
        await ws_manager.broadcast(data)

    message_router.set_ws_callback(ws_broadcast)

    # Workflow registry
    workflow_registry = WorkflowRegistry()
    workflows_dir = config.workflows_dir
    if Path(workflows_dir).exists():
        count = workflow_registry.load_from_directory(workflows_dir)
        logger.info("workflows_loaded", count=count, dir=workflows_dir)
    else:
        logger.warning("workflows_dir_not_found", dir=workflows_dir)

    # Value sets
    value_sets = ValueSetLoader()
    if Path(config.value_sets_dir).exists():
        vs_count = value_sets.load_from_directory(config.value_sets_dir)
        logger.info("value_sets_loaded", count=vs_count)

    # Step handlers
    init_handlers()

    # Engine
    engine = SimulationEngine(
        config=config,
        patient_pool=patient_pool,
        workflow_registry=workflow_registry,
        message_factory=message_factory,
        message_router=message_router,
        state=state,
        clock=clock,
    )

    # Set global deps for web routes
    deps.engine = engine
    deps.patient_pool = patient_pool
    deps.workflow_registry = workflow_registry
    deps.message_factory = message_factory
    deps.message_router = message_router
    deps.message_log = message_log
    deps.state = state
    deps.ws_manager = ws_manager
    deps.auth_config = config.auth

    return {
        "config": config,
        "engine": engine,
        "patient_pool": patient_pool,
        "workflow_registry": workflow_registry,
        "message_factory": message_factory,
        "message_router": message_router,
        "message_log": message_log,
        "state": state,
        "clock": clock,
        "ws_manager": ws_manager,
    }


async def run_app(
    config_path: str | None = None,
    auto_start: bool = False,
) -> None:
    """Run the full application: bootstrap + web server + optional auto-start."""
    config = load_config(config_path)
    if auto_start:
        config.auto_start = True

    components = bootstrap(config)
    engine: SimulationEngine = components["engine"]

    app = create_app()

    server_config = uvicorn.Config(
        app,
        host=config.web.host,
        port=config.web.port,
        log_level="info",
    )
    server = uvicorn.Server(server_config)

    async def start_engine() -> None:
        # Wait a moment for the server to start
        await asyncio.sleep(1)
        if config.auto_start:
            logger.info("auto_starting_simulation")
            await engine.start()

    # Run server and optional auto-start concurrently
    tasks = [server.serve()]
    if config.auto_start:
        tasks.append(start_engine())

    await asyncio.gather(*tasks)
