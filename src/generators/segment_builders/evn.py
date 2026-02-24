"""EVN (Event Type) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_evn(
    event_type: str,
    recorded_datetime: datetime | None = None,
    planned_datetime: datetime | None = None,
    operator_id: str = "",
) -> str:
    """Build EVN segment."""
    recorded = format_timestamp(recorded_datetime)
    planned = format_timestamp(planned_datetime) if planned_datetime else ""

    fields = [
        "EVN",
        event_type,          # EVN.1 Event Type Code
        recorded,            # EVN.2 Recorded Date/Time
        planned,             # EVN.3 Date/Time Planned Event
        "",                  # EVN.4 Event Reason Code
        operator_id,         # EVN.5 Operator ID
    ]
    return "|".join(fields)
