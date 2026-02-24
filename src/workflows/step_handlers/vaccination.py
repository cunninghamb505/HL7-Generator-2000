"""Vaccination step handler -> VXU^V04."""

from __future__ import annotations

import random
from typing import Any

from src.core.patient import Patient
from src.data.identifiers import generate_order_number
from src.workflows.step_handlers.base import Event, StepHandler

VACCINES = [
    ("03", "MMR", "0.5", "mL", "SC", "MSD"),
    ("08", "Hep B Adolescent/Adult", "1.0", "mL", "IM", "SKB"),
    ("10", "IPV", "0.5", "mL", "SC", "PMC"),
    ("20", "DTaP", "0.5", "mL", "IM", "PMC"),
    ("33", "Pneumococcal", "0.5", "mL", "IM", "MSD"),
    ("88", "Influenza", "0.5", "mL", "IM", "SPL"),
    ("115", "Tdap", "0.5", "mL", "IM", "GSK"),
    ("141", "Influenza IIV4", "0.5", "mL", "IM", "SKB"),
    ("150", "Influenza IIV4 Preservative Free", "0.5", "mL", "IM", "SNF"),
    ("207", "COVID-19 mRNA", "0.3", "mL", "IM", "MOD"),
    ("208", "COVID-19 mRNA", "0.3", "mL", "IM", "PFR"),
    ("21", "Varicella", "0.5", "mL", "SC", "MSD"),
    ("52", "Hep A Adult", "1.0", "mL", "IM", "SKB"),
    ("114", "Meningococcal MCV4P", "0.5", "mL", "IM", "SNF"),
    ("187", "Recombinant Zoster", "0.5", "mL", "IM", "GSK"),
]


class VaccinationHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        vaccine_code = params.get("vaccine_code", "")
        vaccine_name = params.get("vaccine_name", "")
        dose = params.get("dose", "")
        dose_units = params.get("dose_units", "")
        route = params.get("route", "")
        manufacturer = params.get("manufacturer", "")

        if not vaccine_code:
            vax = random.choice(VACCINES)
            vaccine_code, vaccine_name, dose, dose_units, route, manufacturer = vax

        lot_number = f"LOT{random.randint(10000, 99999)}"

        return [Event(
            message_type="VXU",
            trigger_event="V04",
            patient=patient,
            kwargs={
                "vaccine_code": vaccine_code,
                "vaccine_name": vaccine_name,
                "dose": dose,
                "dose_units": dose_units,
                "route": route,
                "manufacturer": manufacturer,
                "lot_number": lot_number,
                "site": random.choice(["LA", "RA", "LT", "RT"]),
            },
        )]
