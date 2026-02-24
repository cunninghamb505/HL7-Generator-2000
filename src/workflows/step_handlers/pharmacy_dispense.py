"""Pharmacy dispense step handler -> RDS^O13."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.workflows.step_handlers.base import Event, StepHandler


class PharmacyDispenseHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        # Find the most recent pharmacy order
        order = None
        for o in reversed(patient.orders):
            if o.order_type == "RX":
                order = o
                break

        drug_code = params.get("drug_code", "")
        drug_name = params.get("drug_name", "")
        quantity = params.get("quantity", "1")

        if order and not drug_code:
            drug_code = order.order_code
            drug_name = order.order_name
            order.status = "CM"

        return [Event(
            message_type="RDS",
            trigger_event="O13",
            patient=patient,
            kwargs={
                "order": order,
                "drug_code": drug_code,
                "drug_name": drug_name,
                "quantity": quantity,
            },
        )]
