"""NK1 (Next of Kin) segment builder."""

from __future__ import annotations

from src.core.patient import Patient


def build_nk1(patient: Patient, set_id: int = 1) -> str:
    """Build NK1 segment if patient has next of kin."""
    nok = patient.next_of_kin
    if not nok or not nok.name:
        return ""

    name = nok.name.to_hl7()
    addr = nok.address.to_hl7() if nok.address else ""

    fields = [
        "NK1",
        str(set_id),         # NK1.1 Set ID
        name,                # NK1.2 Name
        nok.relationship,    # NK1.3 Relationship
        addr,                # NK1.4 Address
        nok.phone,           # NK1.5 Phone Number
    ]
    return "|".join(fields)
