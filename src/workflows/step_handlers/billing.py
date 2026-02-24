"""Billing step handler -> DFT^P03."""

from __future__ import annotations

import random
from typing import Any

from src.core.patient import Patient
from src.data.identifiers import generate_order_number
from src.workflows.step_handlers.base import Event, StepHandler

CHARGE_CODES = [
    ("99213", "Office Visit Level 3", "75.00"),
    ("99214", "Office Visit Level 4", "125.00"),
    ("99215", "Office Visit Level 5", "175.00"),
    ("99281", "ED Visit Level 1", "150.00"),
    ("99283", "ED Visit Level 3", "350.00"),
    ("99285", "ED Visit Level 5", "750.00"),
    ("99221", "Initial Hospital Care L1", "200.00"),
    ("99222", "Initial Hospital Care L2", "300.00"),
    ("99223", "Initial Hospital Care L3", "400.00"),
    ("99238", "Hospital Discharge Day", "150.00"),
    ("36415", "Venipuncture", "15.00"),
    ("85025", "CBC with Differential", "25.00"),
    ("80053", "Comprehensive Metabolic Panel", "35.00"),
    ("80048", "Basic Metabolic Panel", "30.00"),
    ("71046", "Chest X-Ray 2 Views", "125.00"),
    ("93000", "ECG 12-Lead", "50.00"),
]


class BillingHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        charge_code = params.get("charge_code", "")
        charge_desc = params.get("charge_description", "")
        amount = params.get("amount", "")
        num_charges = params.get("num_charges", 1)

        transactions = []
        if charge_code:
            transactions.append({
                "transaction_id": generate_order_number("TXN"),
                "transaction_type": "CG",
                "transaction_code": charge_code,
                "transaction_description": charge_desc,
                "amount": amount,
                "department": params.get("department", ""),
            })
        else:
            # Generate random charges
            selected = random.sample(CHARGE_CODES, min(num_charges, len(CHARGE_CODES)))
            for code, desc, amt in selected:
                transactions.append({
                    "transaction_id": generate_order_number("TXN"),
                    "transaction_type": "CG",
                    "transaction_code": code,
                    "transaction_description": desc,
                    "amount": amt,
                })

        return [Event(
            message_type="DFT",
            trigger_event="P03",
            patient=patient,
            kwargs={"transactions": transactions},
        )]
