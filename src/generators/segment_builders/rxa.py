"""RXA (Pharmacy/Treatment Administration) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_rxa(
    admin_code: str,
    admin_name: str,
    dose: str,
    dose_units: str,
    route: str = "IM",
    site: str = "",
    lot_number: str = "",
    manufacturer: str = "",
    coding_system: str = "CVX",
    admin_datetime: datetime | None = None,
    completion_status: str = "CP",
    set_id: int = 0,
    sub_id: int = 1,
) -> str:
    """Build RXA segment for administered medication/vaccine."""
    drug = f"{admin_code}^{admin_name}^{coding_system}"
    ts = format_timestamp(admin_datetime)

    fields = [
        "RXA",
        str(set_id),            # RXA.1 Give Sub-ID Counter
        str(sub_id),            # RXA.2 Administration Sub-ID Counter
        ts,                     # RXA.3 Date/Time Start of Administration
        ts,                     # RXA.4 Date/Time End of Administration
        drug,                   # RXA.5 Administered Code
        dose,                   # RXA.6 Administered Amount
        dose_units,             # RXA.7 Administered Units
        "",                     # RXA.8 Administered Dosage Form
        "",                     # RXA.9 Administration Notes
        "",                     # RXA.10 Administering Provider
        site,                   # RXA.11 Administered-at Location
        "",                     # RXA.12 Administered Per (Time Unit)
        "",                     # RXA.13 Administered Strength
        "",                     # RXA.14 Administered Strength Units
        lot_number,             # RXA.15 Substance Lot Number
        "",                     # RXA.16 Substance Expiration Date
        manufacturer,           # RXA.17 Substance Manufacturer Name
        "",                     # RXA.18 Substance/Treatment Refusal Reason
        "",                     # RXA.19 Indication
        completion_status,      # RXA.20 Completion Status
    ]
    return "|".join(fields)
