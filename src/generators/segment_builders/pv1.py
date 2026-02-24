"""PV1 (Patient Visit) segment builder."""

from __future__ import annotations

from src.core.patient import Patient
from src.utils.hl7_helpers import format_timestamp


def build_pv1(patient: Patient, set_id: int = 1) -> str:
    """Build PV1 segment from patient data."""
    attending = ""
    if patient.attending_doctor_id:
        attending = f"{patient.attending_doctor_id}^{patient.attending_doctor_name}"

    admit_ts = format_timestamp(patient.admit_datetime) if patient.admit_datetime else ""
    discharge_ts = format_timestamp(patient.discharge_datetime) if patient.discharge_datetime else ""

    fields = [
        "PV1",
        str(set_id),                               # PV1.1 Set ID
        patient.patient_class.value,               # PV1.2 Patient Class
        patient.location,                          # PV1.3 Assigned Patient Location
        "",                                        # PV1.4 Admission Type
        "",                                        # PV1.5 Preadmit Number
        "",                                        # PV1.6 Prior Patient Location
        attending,                                 # PV1.7 Attending Doctor
        "",                                        # PV1.8 Referring Doctor
        "",                                        # PV1.9 Consulting Doctor
        "",                                        # PV1.10 Hospital Service
        "",                                        # PV1.11 Temporary Location
        "",                                        # PV1.12 Preadmit Test Indicator
        "",                                        # PV1.13 Re-admission Indicator
        "",                                        # PV1.14 Admit Source
        "",                                        # PV1.15 Ambulatory Status
        "",                                        # PV1.16 VIP Indicator
        "",                                        # PV1.17 Admitting Doctor
        "",                                        # PV1.18 Patient Type
        patient.visit_number,                      # PV1.19 Visit Number
        "",                                        # PV1.20 Financial Class
        "",                                        # PV1.21 Charge Price Indicator
        "",                                        # PV1.22 Courtesy Code
        "",                                        # PV1.23 Credit Rating
        "",                                        # PV1.24 Contract Code
        "",                                        # PV1.25 Contract Effective Date
        "",                                        # PV1.26 Contract Amount
        "",                                        # PV1.27 Contract Period
        "",                                        # PV1.28 Interest Code
        "",                                        # PV1.29 Transfer to Bad Debt Code
        "",                                        # PV1.30 Transfer to Bad Debt Date
        "",                                        # PV1.31 Bad Debt Agency Code
        "",                                        # PV1.32 Bad Debt Transfer Amount
        "",                                        # PV1.33 Bad Debt Recovery Amount
        "",                                        # PV1.34 Delete Account Indicator
        "",                                        # PV1.35 Delete Account Date
        "",                                        # PV1.36 Discharge Disposition
        "",                                        # PV1.37 Discharged to Location
        "",                                        # PV1.38 Diet Type
        "",                                        # PV1.39 Servicing Facility
        "",                                        # PV1.40 Bed Status
        "",                                        # PV1.41 Account Status
        "",                                        # PV1.42 Pending Location
        "",                                        # PV1.43 Prior Temporary Location
        admit_ts,                                  # PV1.44 Admit Date/Time
        discharge_ts,                              # PV1.45 Discharge Date/Time
    ]
    return "|".join(fields)
