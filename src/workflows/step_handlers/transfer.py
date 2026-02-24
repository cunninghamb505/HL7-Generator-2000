"""Transfer step handler -> ADT^A02."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.data.fake_provider import pick_location
from src.workflows.step_handlers.base import Event, StepHandler


class TransferHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        new_location_area = params.get("loc", "")
        new_location = pick_location(new_location_area)

        kwargs: dict[str, Any] = {
            "transfer_reason": params.get("reason", ""),
        }

        patient.location = new_location

        return [Event(
            message_type="ADT",
            trigger_event=params.get("trigger", "A02"),
            patient=patient,
            kwargs=kwargs,
        )]
