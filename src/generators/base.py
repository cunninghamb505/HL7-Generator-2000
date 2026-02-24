"""Base message generator ABC."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.core.config import FacilityConfig
from src.core.patient import Patient


class MessageGenerator(ABC):
    """Base class for HL7 message generators."""

    def __init__(self, facility: FacilityConfig, hl7_version: str = "2.5.1"):
        self.facility = facility
        self.hl7_version = hl7_version

    @abstractmethod
    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        """Generate a complete HL7 message string.

        Returns segments joined by \\r (carriage return) as per HL7 spec.
        """
        ...

    @property
    @abstractmethod
    def message_type(self) -> str:
        """The 3-letter message type code (e.g., 'ADT', 'ORM')."""
        ...

    @property
    @abstractmethod
    def supported_triggers(self) -> list[str]:
        """List of supported trigger event codes."""
        ...

    def _join_segments(self, segments: list[str]) -> str:
        """Join non-empty segments with CR."""
        return "\r".join(s for s in segments if s)
