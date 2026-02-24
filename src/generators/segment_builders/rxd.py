"""RXD (Pharmacy/Treatment Dispense) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_rxd(
    dispense_code: str,
    dispense_name: str,
    actual_quantity: str,
    actual_units: str = "",
    prescription_number: str = "",
    coding_system: str = "NDC",
    dispense_datetime: datetime | None = None,
) -> str:
    """Build RXD segment for pharmacy dispense."""
    drug = f"{dispense_code}^{dispense_name}^{coding_system}"
    ts = format_timestamp(dispense_datetime)

    fields = [
        "RXD",
        "",                     # RXD.1 Dispense Sub-ID Counter
        drug,                   # RXD.2 Dispense/Give Code
        ts,                     # RXD.3 Date/Time Dispensed
        actual_quantity,        # RXD.4 Actual Dispense Amount
        actual_units,           # RXD.5 Actual Dispense Units
        "",                     # RXD.6 Actual Dosage Form
        prescription_number,    # RXD.7 Prescription Number
    ]
    return "|".join(fields)
