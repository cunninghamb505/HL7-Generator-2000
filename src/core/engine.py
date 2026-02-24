"""Main simulation engine - start, stop, pause, and manage workflow execution."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import structlog

from src.core.clock import SimulationClock
from src.core.config import SimulatorConfig
from src.core.patient_pool import PatientPool
from src.core.scheduler import Scheduler
from src.core.state import SimulationState, SimulationStatus
from src.generators.message_factory import MessageFactory
from src.workflows.workflow_engine import WorkflowEngine
from src.workflows.workflow_registry import WorkflowRegistry
from src.transport.message_router import MessageRouter

logger = structlog.get_logger(__name__)


class SimulationEngine:
    def __init__(
        self,
        config: SimulatorConfig,
        patient_pool: PatientPool,
        workflow_registry: WorkflowRegistry,
        message_factory: MessageFactory,
        message_router: MessageRouter,
        state: SimulationState,
        clock: SimulationClock,
    ):
        self._config = config
        self._pool = patient_pool
        self._registry = workflow_registry
        self._factory = message_factory
        self._router = message_router
        self._state = state
        self._clock = clock
        self._scheduler = Scheduler(config.scheduling)
        self._workflow_engine = WorkflowEngine(
            message_factory, message_router, clock, state,
        )
        self._main_task: asyncio.Task[Any] | None = None
        self._active_tasks: set[asyncio.Task[Any]] = set()

    async def start(self) -> None:
        """Start the simulation."""
        if self._state.status == SimulationStatus.RUNNING:
            logger.info("engine_already_running")
            return

        self._state.status = SimulationStatus.RUNNING
        self._state.start_time = time.time()
        self._clock.resume()

        logger.info(
            "engine_started",
            rate=self._scheduler.current_rate,
            workflows=self._registry.count,
            patients=self._pool.total_count,
        )

        self._main_task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        """Stop the simulation."""
        self._state.status = SimulationStatus.STOPPED

        if self._main_task:
            self._main_task.cancel()
            try:
                await self._main_task
            except asyncio.CancelledError:
                pass
            self._main_task = None

        # Cancel all active workflow tasks
        for task in list(self._active_tasks):
            task.cancel()
        self._active_tasks.clear()

        await self._router.close_all()
        logger.info("engine_stopped")

    async def pause(self) -> None:
        """Pause the simulation."""
        self._state.status = SimulationStatus.PAUSED
        self._clock.pause()
        logger.info("engine_paused")

    async def resume(self) -> None:
        """Resume a paused simulation."""
        if self._state.status != SimulationStatus.PAUSED:
            return
        self._state.status = SimulationStatus.RUNNING
        self._clock.resume()
        logger.info("engine_resumed")

    async def trigger_workflow(self, workflow_name: str) -> dict[str, Any]:
        """Manually trigger a specific workflow."""
        workflow = self._registry.get(workflow_name)
        if not workflow:
            return {"error": f"Workflow not found: {workflow_name}"}

        patient = self._pool.acquire_patient()
        if not patient:
            return {"error": "No patients available"}

        task = asyncio.create_task(
            self._run_workflow(workflow_name, patient.mrn)
        )
        self._active_tasks.add(task)
        task.add_done_callback(self._active_tasks.discard)

        return {
            "status": "started",
            "workflow": workflow_name,
            "patient_mrn": patient.mrn,
        }

    def set_rate(self, rate: float) -> None:
        """Update the message generation rate."""
        self._scheduler.set_rate(rate)
        self._state.current_rate = rate
        logger.info("rate_changed", rate=rate)

    @property
    def scheduler(self) -> Scheduler:
        return self._scheduler

    async def _run_loop(self) -> None:
        """Main simulation loop."""
        try:
            while self._state.status == SimulationStatus.RUNNING:
                if self._state.status == SimulationStatus.PAUSED:
                    await asyncio.sleep(0.5)
                    continue

                if self._registry.count == 0:
                    logger.warning("no_workflows_loaded")
                    await asyncio.sleep(5)
                    continue

                # Pick a random workflow and patient
                workflow = self._registry.pick_random()
                if not workflow:
                    await asyncio.sleep(1)
                    continue

                patient = self._pool.acquire_patient()
                if not patient:
                    await asyncio.sleep(1)
                    continue

                # Launch workflow as a concurrent task
                task = asyncio.create_task(
                    self._run_workflow(workflow.name, patient.mrn)
                )
                self._active_tasks.add(task)
                task.add_done_callback(self._active_tasks.discard)

                # Wait based on rate
                interval = self._scheduler.jittered_interval()
                await asyncio.sleep(interval)

        except asyncio.CancelledError:
            pass

    async def _run_workflow(self, workflow_name: str, patient_mrn: str) -> None:
        """Execute a single workflow for a patient."""
        workflow = self._registry.get(workflow_name)
        patient = self._pool.get_patient(patient_mrn)
        if not workflow or not patient:
            return

        try:
            await self._workflow_engine.execute_workflow(workflow, patient)
        except Exception as e:
            logger.error(
                "workflow_execution_error",
                workflow=workflow_name,
                patient=patient_mrn,
                error=str(e),
            )
        finally:
            self._pool.release_patient(patient_mrn)
