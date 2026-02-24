"""PV2 (Patient Visit - Additional Information) segment builder."""

from __future__ import annotations

from src.core.patient import Patient
from src.utils.hl7_helpers import format_timestamp


def build_pv2(
    patient: Patient,
    admit_reason: str = "",
    transfer_reason: str = "",
    visit_description: str = "",
) -> str:
    """Build PV2 segment."""
    expected_admit = format_timestamp(patient.admit_datetime) if patient.admit_datetime else ""

    fields = [
        "PV2",
        "",                    # PV2.1 Prior Pending Location
        "",                    # PV2.2 Accommodation Code
        admit_reason,          # PV2.3 Admit Reason
        transfer_reason,       # PV2.4 Transfer Reason
        "",                    # PV2.5 Patient Valuables
        "",                    # PV2.6 Patient Valuables Location
        "",                    # PV2.7 Visit User Code
        expected_admit,        # PV2.8 Expected Admit Date/Time
        "",                    # PV2.9 Expected Discharge Date/Time
        "",                    # PV2.10 Estimated Length of Inpatient Stay
        "",                    # PV2.11 Actual Length of Inpatient Stay
        visit_description,     # PV2.12 Visit Description
    ]
    return "|".join(fields)
