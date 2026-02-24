"""Dependency injection helpers for FastAPI routes."""

from __future__ import annotations

from typing import Any

from src.core.config import AuthConfig
from src.core.engine import SimulationEngine
from src.core.patient_pool import PatientPool
from src.core.state import SimulationState
from src.generators.message_factory import MessageFactory
from src.workflows.workflow_registry import WorkflowRegistry
from src.transport.message_router import MessageRouter
from src.utils.message_log import MessageLog
from src.web.websocket import WebSocketManager


class AppDependencies:
    """Container for all application dependencies."""

    def __init__(self) -> None:
        self.engine: SimulationEngine | None = None
        self.patient_pool: PatientPool | None = None
        self.workflow_registry: WorkflowRegistry | None = None
        self.message_factory: MessageFactory | None = None
        self.message_router: MessageRouter | None = None
        self.message_log: MessageLog | None = None
        self.state: SimulationState | None = None
        self.ws_manager: WebSocketManager | None = None
        self.auth_config: AuthConfig | None = None


# Global singleton - set during app bootstrap
deps = AppDependencies()
