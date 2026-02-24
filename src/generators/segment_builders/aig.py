"""AIG (Appointment Information - General Resource) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_aig(
    set_id: int = 1,
    resource_id: str = "",
    resource_type: str = "",
    resource_group: str = "",
    start_datetime: datetime | None = None,
    duration: str = "",
    duration_units: str = "min",
) -> str:
    """Build AIG segment for scheduling general resources."""
    ts = format_timestamp(start_datetime) if start_datetime else ""

    fields = [
        "AIG",
        str(set_id),       # AIG.1 Set ID
        "",                # AIG.2 Segment Action Code
        resource_id,       # AIG.3 Resource ID
        resource_type,     # AIG.4 Resource Type
        resource_group,    # AIG.5 Resource Group
        "",                # AIG.6 Resource Quantity
        "",                # AIG.7 Resource Quantity Units
        ts,                # AIG.8 Start Date/Time
        "",                # AIG.9 Start Date/Time Offset
        "",                # AIG.10 Start Date/Time Offset Units
        duration,          # AIG.11 Duration
        duration_units,    # AIG.12 Duration Units
    ]
    return "|".join(fields)
