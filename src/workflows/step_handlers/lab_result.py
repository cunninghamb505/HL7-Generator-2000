"""Lab result step handler -> ORU^R01."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.data.clinical_data import generate_lab_results
from src.workflows.step_handlers.base import Event, StepHandler


class LabResultHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        profile = params.get("order_profile", "")
        result_status = params.get("result_status", "F")
        abnormal_rate = params.get("abnormal_rate", 0.15)

        # Find matching order
        order = None
        for o in patient.orders:
            if o.order_name and profile.upper() in o.order_name.upper():
                order = o
                break
            if o.order_code and profile.upper() == o.order_code:
                order = o
                break

        if order is None and patient.orders:
            order = patient.orders[-1]

        # Generate results
        results = generate_lab_results(
            order_profile=profile or (order.order_name if order else "CMP"),
            abnormal_rate=abnormal_rate,
        )

        if order:
            order.status = "CM"
            order.results = results

        return [Event(
            message_type="ORU",
            trigger_event="R01",
            patient=patient,
            kwargs={
                "order": order,
                "results": results,
                "result_status": result_status,
            },
        )]
