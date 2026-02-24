"""Pharmacy order step handler -> RDE^O11."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Any

from src.core.patient import Order, Patient
from src.data.identifiers import generate_filler_order_number, generate_placer_order_number
from src.workflows.step_handlers.base import Event, StepHandler

MEDICATIONS = [
    ("00002-4462", "Lisinopril 10mg", "10", "mg", "PO"),
    ("00074-3799", "Amoxicillin 500mg", "500", "mg", "PO"),
    ("00069-1530", "Metformin 500mg", "500", "mg", "PO"),
    ("00006-0749", "Atorvastatin 20mg", "20", "mg", "PO"),
    ("00093-7180", "Metoprolol 25mg", "25", "mg", "PO"),
    ("00378-1800", "Omeprazole 20mg", "20", "mg", "PO"),
    ("65862-0176", "Amlodipine 5mg", "5", "mg", "PO"),
    ("00781-1506", "Azithromycin 250mg", "250", "mg", "PO"),
    ("00591-5613", "Furosemide 40mg", "40", "mg", "PO"),
    ("00069-0980", "Ceftriaxone 1g", "1", "g", "IV"),
    ("00409-1176", "Morphine 4mg", "4", "mg", "IV"),
    ("00074-4963", "Vancomycin 1g", "1", "g", "IV"),
    ("00009-0775", "Heparin 5000 Units", "5000", "Units", "SC"),
    ("00002-7515", "Insulin Lispro", "10", "Units", "SC"),
]


class PharmacyOrderHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        drug_code = params.get("drug_code", "")
        drug_name = params.get("drug_name", "")
        dose = params.get("dose", "")
        dose_units = params.get("dose_units", "mg")
        route = params.get("route", "PO")

        if not drug_code:
            med = random.choice(MEDICATIONS)
            drug_code, drug_name, dose, dose_units, route = med

        order = Order(
            placer_order_number=generate_placer_order_number(),
            filler_order_number=generate_filler_order_number(),
            order_type="RX",
            order_code=drug_code,
            order_name=drug_name,
            priority=params.get("priority", "R"),
            status="IP",
            order_datetime=datetime.now(),
        )
        patient.orders.append(order)

        return [Event(
            message_type="RDE",
            trigger_event="O11",
            patient=patient,
            kwargs={
                "order": order,
                "drug_code": drug_code,
                "drug_name": drug_name,
                "dose": dose,
                "dose_units": dose_units,
                "route": route,
            },
        )]
