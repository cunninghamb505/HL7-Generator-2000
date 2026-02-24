"""DG1 (Diagnosis) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.core.patient import Diagnosis
from src.utils.hl7_helpers import format_timestamp


def build_dg1(diagnosis: Diagnosis, set_id: int = 1, timestamp: datetime | None = None) -> str:
    """Build DG1 segment from diagnosis data."""
    ts = format_timestamp(timestamp)

    fields = [
        "DG1",
        str(set_id),                                           # DG1.1 Set ID
        "",                                                    # DG1.2 Diagnosis Coding Method
        f"{diagnosis.code}^{diagnosis.description}^{diagnosis.coding_system}",  # DG1.3 Diagnosis Code
        diagnosis.description,                                 # DG1.4 Diagnosis Description
        ts,                                                    # DG1.5 Diagnosis Date/Time
        diagnosis.diagnosis_type,                              # DG1.6 Diagnosis Type
    ]
    return "|".join(fields)


def build_dg1_segments(diagnoses: list[Diagnosis], timestamp: datetime | None = None) -> list[str]:
    return [build_dg1(d, i + 1, timestamp) for i, d in enumerate(diagnoses)]
