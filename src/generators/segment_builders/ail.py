"""AIL (Appointment Information - Location Resource) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_ail(
    set_id: int = 1,
    location_resource_id: str = "",
    location_type: str = "",
    start_datetime: datetime | None = None,
    duration: str = "",
    duration_units: str = "min",
) -> str:
    """Build AIL segment for scheduling location resources."""
    ts = format_timestamp(start_datetime) if start_datetime else ""

    fields = [
        "AIL",
        str(set_id),             # AIL.1 Set ID
        "",                      # AIL.2 Segment Action Code
        location_resource_id,    # AIL.3 Location Resource ID
        location_type,           # AIL.4 Location Type
        "",                      # AIL.5 Location Group
        ts,                      # AIL.6 Start Date/Time
        "",                      # AIL.7 Start Date/Time Offset
        "",                      # AIL.8 Start Date/Time Offset Units
        duration,                # AIL.9 Duration
        duration_units,          # AIL.10 Duration Units
    ]
    return "|".join(fields)
