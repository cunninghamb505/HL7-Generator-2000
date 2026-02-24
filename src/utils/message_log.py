"""In-memory ring buffer for message logging with search."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any


@dataclass
class LogEntry:
    timestamp: float
    message_type: str
    trigger_event: str
    patient_mrn: str
    patient_name: str
    raw_message: str
    destination: str = ""
    ack_status: str = ""
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "timestamp_formatted": time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(self.timestamp)
            ),
            "message_type": self.message_type,
            "trigger_event": self.trigger_event,
            "full_type": f"{self.message_type}^{self.trigger_event}",
            "patient_mrn": self.patient_mrn,
            "patient_name": self.patient_name,
            "raw_message": self.raw_message,
            "destination": self.destination,
            "ack_status": self.ack_status,
            "error": self.error,
        }


class MessageLog:
    def __init__(self, max_size: int = 10000):
        self._buffer: deque[LogEntry] = deque(maxlen=max_size)
        self._max_size = max_size

    def add(self, entry: LogEntry) -> None:
        self._buffer.append(entry)

    def get_recent(self, count: int = 50) -> list[dict[str, Any]]:
        entries = list(self._buffer)[-count:]
        entries.reverse()
        return [e.to_dict() for e in entries]

    def search(
        self,
        query: str = "",
        message_type: str = "",
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        results = list(self._buffer)
        results.reverse()

        if message_type:
            results = [e for e in results if message_type in e.message_type]

        if query:
            q = query.lower()
            results = [
                e for e in results
                if q in e.raw_message.lower()
                or q in e.patient_mrn.lower()
                or q in e.patient_name.lower()
            ]

        return [e.to_dict() for e in results[offset:offset + limit]]

    @property
    def total_count(self) -> int:
        return len(self._buffer)

    def clear(self) -> None:
        self._buffer.clear()
