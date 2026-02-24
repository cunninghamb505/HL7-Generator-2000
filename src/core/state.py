"""Metrics and simulation state counters."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SimulationStatus(str, Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"


@dataclass
class SimulationState:
    status: SimulationStatus = SimulationStatus.STOPPED
    messages_sent: int = 0
    messages_by_type: dict[str, int] = field(default_factory=dict)
    active_workflows: int = 0
    completed_workflows: int = 0
    errors: int = 0
    start_time: float | None = None
    current_rate: float = 0.0
    _rate_window: list[float] = field(default_factory=list)

    def record_message(self, message_type: str) -> None:
        self.messages_sent += 1
        self.messages_by_type[message_type] = (
            self.messages_by_type.get(message_type, 0) + 1
        )
        now = time.time()
        self._rate_window.append(now)
        cutoff = now - 60
        self._rate_window = [t for t in self._rate_window if t > cutoff]
        self.current_rate = len(self._rate_window)

    def record_error(self) -> None:
        self.errors += 1

    def reset(self) -> None:
        self.messages_sent = 0
        self.messages_by_type.clear()
        self.active_workflows = 0
        self.completed_workflows = 0
        self.errors = 0
        self.start_time = None
        self.current_rate = 0.0
        self._rate_window.clear()

    def to_dict(self) -> dict[str, Any]:
        uptime = 0.0
        if self.start_time:
            uptime = time.time() - self.start_time
        return {
            "status": self.status.value,
            "messages_sent": self.messages_sent,
            "messages_by_type": dict(self.messages_by_type),
            "active_workflows": self.active_workflows,
            "completed_workflows": self.completed_workflows,
            "errors": self.errors,
            "current_rate": round(self.current_rate, 1),
            "uptime_seconds": round(uptime, 1),
        }
