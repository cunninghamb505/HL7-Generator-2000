"""Lab order step handler -> ORM^O01."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.core.patient import Order, Patient
from src.data.clinical_data import get_order_profile_code
from src.data.identifiers import generate_filler_order_number, generate_placer_order_number
from src.workflows.step_handlers.base import Event, StepHandler


class LabOrderHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        profile = params.get("order_profile", "CMP")
        priority = params.get("priority", "R")

        order_code, order_name = get_order_profile_code(profile)

        order = Order(
            placer_order_number=generate_placer_order_number(),
            filler_order_number=generate_filler_order_number(),
            order_type="LAB",
            order_code=order_code,
            order_name=order_name,
            priority=priority,
            status="IP",
            order_datetime=datetime.now(),
        )

        patient.orders.append(order)

        return [Event(
            message_type="ORM",
            trigger_event="O01",
            patient=patient,
            kwargs={"order": order, "order_control": "NW"},
        )]
