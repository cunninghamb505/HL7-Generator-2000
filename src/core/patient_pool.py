"""Patient pool management: idle, active, and retired patients."""

from __future__ import annotations

import random
from typing import Any

from src.core.patient import Patient, PatientStatus
from src.data.fake_provider import generate_patient


class PatientPool:
    def __init__(self, pool_size: int = 500, min_age: int = 1, max_age: int = 95, insurance_rate: float = 0.85):
        self._pool_size = pool_size
        self._min_age = min_age
        self._max_age = max_age
        self._insurance_rate = insurance_rate
        self._patients: dict[str, Patient] = {}
        self._idle: list[str] = []
        self._active: set[str] = set()

    def initialize(self) -> None:
        """Generate the initial patient pool."""
        for _ in range(self._pool_size):
            patient = generate_patient(self._min_age, self._max_age, self._insurance_rate)
            self._patients[patient.mrn] = patient
            self._idle.append(patient.mrn)

    def acquire_patient(self) -> Patient | None:
        """Get an idle patient and mark them active."""
        if not self._idle:
            # Generate a new patient if pool is exhausted
            patient = generate_patient(self._min_age, self._max_age, self._insurance_rate)
            self._patients[patient.mrn] = patient
            self._idle.append(patient.mrn)

        mrn = random.choice(self._idle)
        self._idle.remove(mrn)
        self._active.add(mrn)
        patient = self._patients[mrn]
        patient.status = PatientStatus.ACTIVE
        return patient

    def release_patient(self, mrn: str) -> None:
        """Return a patient to idle pool."""
        if mrn in self._active:
            self._active.discard(mrn)
            patient = self._patients[mrn]
            patient.status = PatientStatus.IDLE
            patient.active_workflow = ""
            patient.workflow_step = 0
            patient.orders.clear()
            patient.diagnoses.clear()
            patient.location = ""
            patient.admit_datetime = None
            patient.discharge_datetime = None
            self._idle.append(mrn)

    def get_patient(self, mrn: str) -> Patient | None:
        return self._patients.get(mrn)

    @property
    def idle_count(self) -> int:
        return len(self._idle)

    @property
    def active_count(self) -> int:
        return len(self._active)

    @property
    def total_count(self) -> int:
        return len(self._patients)

    def list_patients(self, status: str | None = None, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
        patients = list(self._patients.values())
        if status:
            patients = [p for p in patients if p.status.value == status]
        patients.sort(key=lambda p: p.mrn)
        return [p.to_dict() for p in patients[offset:offset + limit]]
