"""BAR (Billing Account Record) step handler -> BAR^P01."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.workflows.step_handlers.base import Event, StepHandler


class BARHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        trigger = params.get("trigger", "P01")
        return [Event(
            message_type="BAR",
            trigger_event=trigger,
            patient=patient,
        )]
