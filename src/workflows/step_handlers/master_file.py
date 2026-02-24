"""Master file step handler -> MFN^M01-M13."""

from __future__ import annotations

import random
from typing import Any

from src.core.patient import Patient
from src.data.identifiers import generate_order_number
from src.workflows.step_handlers.base import Event, StepHandler


class MasterFileHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        trigger = params.get("trigger", "M01")
        master_file_id = params.get("master_file_id", "LOC")

        entries = params.get("entries", [])
        if not entries:
            entries = [
                {
                    "event_code": "MAD",
                    "control_id": generate_order_number("MFN"),
                    "primary_key": f"ENTRY{random.randint(1000, 9999)}",
                }
            ]

        return [Event(
            message_type="MFN",
            trigger_event=trigger,
            patient=patient,
            kwargs={
                "master_file_id": master_file_id,
                "entries": entries,
            },
        )]
