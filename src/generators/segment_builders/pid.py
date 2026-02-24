"""PID (Patient Identification) segment builder."""

from __future__ import annotations

from src.core.patient import Patient
from src.utils.hl7_helpers import format_date


def build_pid(patient: Patient, set_id: int = 1) -> str:
    """Build PID segment from patient data."""
    fields = [
        "PID",
        str(set_id),                              # PID.1 Set ID
        "",                                        # PID.2 Patient ID (external)
        f"{patient.mrn}^^^MRN^MR",                # PID.3 Patient Identifier List
        "",                                        # PID.4 Alternate Patient ID
        patient.name.to_hl7(),                     # PID.5 Patient Name
        "",                                        # PID.6 Mother's Maiden Name
        format_date(patient.date_of_birth),        # PID.7 Date of Birth
        patient.gender,                            # PID.8 Sex
        "",                                        # PID.9 Patient Alias
        patient.race,                              # PID.10 Race
        patient.address.to_hl7(),                  # PID.11 Address
        "",                                        # PID.12 County Code
        patient.phone_home,                        # PID.13 Phone - Home
        patient.phone_work,                        # PID.14 Phone - Business
        patient.language,                          # PID.15 Primary Language
        patient.marital_status,                    # PID.16 Marital Status
        patient.religion,                          # PID.17 Religion
        patient.account_number,                    # PID.18 Patient Account Number
        patient.ssn,                               # PID.19 SSN
        "",                                        # PID.20 Driver's License
        "",                                        # PID.21 Mother's Identifier
        patient.ethnicity,                         # PID.22 Ethnic Group
    ]
    return "|".join(fields)
