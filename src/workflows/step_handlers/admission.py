"""Admission/Registration step handler -> ADT^A01/A04/A05."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from src.core.patient import Diagnosis, Patient, PatientClass, PatientStatus
from src.data.fake_provider import pick_doctor, pick_location
from src.data.identifiers import generate_account_number, generate_visit_number
from src.workflows.step_handlers.base import Event, StepHandler


class AdmissionHandler(StepHandler):
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        patient_class = params.get("patient_class", "I")
        location_area = params.get("loc", "")
        trigger = params.get("trigger", "")

        # Update patient state
        patient.status = PatientStatus.ACTIVE
        patient.patient_class = PatientClass(patient_class)
        patient.location = pick_location(location_area)
        patient.admit_datetime = datetime.now()
        patient.account_number = generate_account_number()
        patient.visit_number = generate_visit_number()

        # Assign attending doctor
        doc_id, doc_name = pick_doctor()
        patient.attending_doctor_id = doc_id
        patient.attending_doctor_name = doc_name

        # Add diagnosis if provided
        dx_code = params.get("diagnosis_code", "")
        dx_desc = params.get("diagnosis_desc", "")
        if dx_code:
            patient.diagnoses.append(Diagnosis(
                code=dx_code,
                description=dx_desc,
                diagnosis_type="A",
            ))

        # Determine trigger event
        if not trigger:
            if patient_class == "E":
                trigger = "A04"  # ER Registration
            elif patient_class == "P":
                trigger = "A05"  # Pre-admit
            else:
                trigger = "A01"  # Admit

        return [Event(
            message_type="ADT",
            trigger_event=trigger,
            patient=patient,
        )]
