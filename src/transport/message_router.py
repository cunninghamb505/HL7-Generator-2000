"""Message router - sends messages to multiple destinations."""

from __future__ import annotations

import asyncio
import time
from typing import Any

import structlog

from src.core.config import DestinationConfig
from src.core.patient import Patient
from src.transport.console_writer import ConsoleWriter
from src.transport.file_writer import FileWriter
from src.transport.mllp_client import MLLPClient
from src.transport.tls_utils import build_ssl_context
from src.utils.message_log import LogEntry, MessageLog
from src.validators.message_validator import validate_message

logger = structlog.get_logger(__name__)


class MessageRouter:
    def __init__(self, message_log: MessageLog):
        self._destinations: dict[str, Any] = {}
        self._configs: dict[str, DestinationConfig] = {}
        self._message_log = message_log
        self._ws_callback: Any = None

    def add_destination(self, config: DestinationConfig) -> None:
        self._configs[config.name] = config
        if config.type == "mllp":
            ssl_ctx = build_ssl_context(config) if config.tls_enabled else None
            self._destinations[config.name] = MLLPClient(
                host=config.host,
                port=config.port,
                name=config.name,
                ssl_context=ssl_ctx,
            )
        elif config.type == "file":
            self._destinations[config.name] = FileWriter(
                output_dir=config.file_path or "output",
            )
        elif config.type == "console":
            self._destinations[config.name] = ConsoleWriter()

    def set_ws_callback(self, callback: Any) -> None:
        """Set WebSocket broadcast callback for live dashboard feed."""
        self._ws_callback = callback

    async def route(
        self,
        message: str,
        patient: Patient,
        message_type: str = "",
        trigger_event: str = "",
    ) -> bool:
        """Route a message to all enabled destinations."""
        success = False
        patient_name = f"{patient.name.given} {patient.name.family}"

        for name, dest in self._destinations.items():
            config = self._configs.get(name)
            if config and not config.enabled:
                continue

            try:
                result = await dest.send(message)
                if result is not None and result is not False:
                    success = True
                    dest_name = name
                else:
                    dest_name = f"{name}(failed)"
            except Exception as e:
                logger.error("route_failed", destination=name, error=str(e))
                dest_name = f"{name}(error)"

        # Validate message
        validation = validate_message(message, message_type)
        validation_errors = validation.errors if not validation.valid else []
        if validation_errors:
            logger.warning(
                "message_validation_failed",
                message_type=message_type,
                errors=validation_errors,
            )

        # Log the message
        entry = LogEntry(
            timestamp=time.time(),
            message_type=message_type,
            trigger_event=trigger_event,
            patient_mrn=patient.mrn,
            patient_name=patient_name,
            raw_message=message,
            destination=", ".join(self._destinations.keys()),
            validation_errors=validation_errors,
        )
        self._message_log.add(entry)

        # Broadcast via WebSocket if available
        if self._ws_callback:
            try:
                await self._ws_callback(entry.to_dict())
            except Exception:
                pass

        return success

    async def close_all(self) -> None:
        for name, dest in self._destinations.items():
            if hasattr(dest, "close"):
                await dest.close()

    def list_destinations(self) -> list[dict[str, Any]]:
        result = []
        for name, config in self._configs.items():
            dest = self._destinations.get(name)
            connected = False
            if hasattr(dest, "is_connected"):
                connected = dest.is_connected
            result.append({
                "name": name,
                "type": config.type,
                "host": config.host,
                "port": config.port,
                "enabled": config.enabled,
                "connected": connected,
                "file_path": config.file_path,
                "tls_enabled": config.tls_enabled,
            })
        return result

    def update_destination(self, name: str, **kwargs: Any) -> bool:
        config = self._configs.get(name)
        if not config:
            return False
        for key, value in kwargs.items():
            if hasattr(config, key):
                setattr(config, key, value)
        return True

    def remove_destination(self, name: str) -> bool:
        if name in self._destinations:
            del self._destinations[name]
            del self._configs[name]
            return True
        return False
