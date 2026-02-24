"""Discharge step handler -> ADT^A03."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.core.patient import Patient, PatientStatus
from src.workflows.step_handlers.base import Event, StepHandler


class DischargeHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        patient.discharge_datetime = datetime.now()
        patient.status = PatientStatus.DISCHARGED

        trigger = params.get("trigger", "A03")

        return [Event(
            message_type="ADT",
            trigger_event=trigger,
            patient=patient,
        )]
