"""Scheduling step handler -> SIU^S12-S26."""

from __future__ import annotations

import random
from datetime import datetime, timedelta
from typing import Any

from src.core.patient import Patient
from src.data.identifiers import generate_order_number
from src.workflows.step_handlers.base import Event, StepHandler

APPOINTMENT_TYPES = [
    "ROUTINE", "FOLLOWUP", "URGENT", "NEWPATIENT",
    "PROCEDURE", "CONSULTATION", "PHYSICAL",
]

APPOINTMENT_REASONS = [
    "Annual Physical", "Follow-up Visit", "Lab Review",
    "Medication Check", "New Patient Evaluation",
    "Post-Op Follow-up", "Chronic Disease Management",
]


class SchedulingHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        trigger = params.get("trigger", "S12")
        duration = params.get("duration", "30")
        appt_type = params.get("appointment_type", random.choice(APPOINTMENT_TYPES))
        reason = params.get("appointment_reason", random.choice(APPOINTMENT_REASONS))

        # Schedule 1-14 days in the future
        start = datetime.now() + timedelta(
            days=random.randint(1, 14),
            hours=random.randint(8, 16),
            minutes=random.choice([0, 15, 30, 45]),
        )
        end = start + timedelta(minutes=int(duration))

        return [Event(
            message_type="SIU",
            trigger_event=trigger,
            patient=patient,
            kwargs={
                "appointment_id": generate_order_number("APT"),
                "appointment_type": appt_type,
                "appointment_reason": reason,
                "duration": duration,
                "start_datetime": start,
                "end_datetime": end,
            },
        )]
