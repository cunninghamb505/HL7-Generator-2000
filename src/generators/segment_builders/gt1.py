"""GT1 (Guarantor) segment builder."""

from __future__ import annotations

from src.core.patient import Patient
from src.utils.hl7_helpers import format_date


def build_gt1(patient: Patient, set_id: int = 1) -> str:
    """Build GT1 segment (guarantor = patient self)."""
    fields = [
        "GT1",
        str(set_id),                        # GT1.1 Set ID
        "",                                 # GT1.2 Guarantor Number
        patient.name.to_hl7(),             # GT1.3 Guarantor Name
        "",                                 # GT1.4 Guarantor Spouse Name
        patient.address.to_hl7(),          # GT1.5 Guarantor Address
        patient.phone_home,                # GT1.6 Guarantor Phone - Home
        patient.phone_work,                # GT1.7 Guarantor Phone - Business
        format_date(patient.date_of_birth), # GT1.8 Guarantor Date of Birth
        patient.gender,                     # GT1.9 Guarantor Sex
        "",                                 # GT1.10 Guarantor Type
        "SEL",                              # GT1.11 Guarantor Relationship
    ]
    return "|".join(fields)
