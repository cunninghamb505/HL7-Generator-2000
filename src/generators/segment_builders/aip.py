"""AIP (Appointment Information - Personnel Resource) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_aip(
    set_id: int = 1,
    resource_id: str = "",
    resource_name: str = "",
    resource_type: str = "",
    start_datetime: datetime | None = None,
    duration: str = "",
    duration_units: str = "min",
) -> str:
    """Build AIP segment for scheduling personnel resources."""
    ts = format_timestamp(start_datetime) if start_datetime else ""
    person = f"{resource_id}^{resource_name}" if resource_id else ""

    fields = [
        "AIP",
        str(set_id),       # AIP.1 Set ID
        "",                # AIP.2 Segment Action Code
        person,            # AIP.3 Personnel Resource ID
        resource_type,     # AIP.4 Resource Type
        "",                # AIP.5 Resource Group
        ts,                # AIP.6 Start Date/Time
        "",                # AIP.7 Start Date/Time Offset
        "",                # AIP.8 Start Date/Time Offset Units
        duration,          # AIP.9 Duration
        duration_units,    # AIP.10 Duration Units
    ]
    return "|".join(fields)
