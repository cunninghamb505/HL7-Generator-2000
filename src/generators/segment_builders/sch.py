"""SCH (Scheduling Activity Information) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_sch(
    placer_appointment_id: str = "",
    filler_appointment_id: str = "",
    event_reason: str = "",
    appointment_type: str = "",
    appointment_duration: str = "",
    duration_units: str = "min",
    appointment_timing: str = "",
    start_datetime: datetime | None = None,
    end_datetime: datetime | None = None,
    placer_contact: str = "",
    filler_contact: str = "",
    filler_status_code: str = "",
) -> str:
    """Build SCH segment for scheduling messages."""
    start_ts = format_timestamp(start_datetime) if start_datetime else ""
    end_ts = format_timestamp(end_datetime) if end_datetime else ""

    # Build timing quantity: start^end
    timing = f"{start_ts}^{end_ts}" if start_ts else ""

    fields = [
        "SCH",
        placer_appointment_id,   # SCH.1 Placer Appointment ID
        filler_appointment_id,   # SCH.2 Filler Appointment ID
        "",                      # SCH.3 Occurrence Number
        "",                      # SCH.4 Placer Group Number
        "",                      # SCH.5 Schedule ID
        event_reason,            # SCH.6 Event Reason
        "",                      # SCH.7 Appointment Reason
        appointment_type,        # SCH.8 Appointment Type
        appointment_duration,    # SCH.9 Appointment Duration
        duration_units,          # SCH.10 Appointment Duration Units
        timing,                  # SCH.11 Appointment Timing Quantity
        placer_contact,          # SCH.12 Placer Contact Person
        "",                      # SCH.13 Placer Contact Phone
        "",                      # SCH.14 Placer Contact Address
        "",                      # SCH.15 Placer Contact Location
        filler_contact,          # SCH.16 Filler Contact Person
        "",                      # SCH.17 Filler Contact Phone
        "",                      # SCH.18 Filler Contact Address
        "",                      # SCH.19 Filler Contact Location
        "",                      # SCH.20 Entered By Person
        "",                      # SCH.21 Entered By Phone
        "",                      # SCH.22 Entered By Location
        "",                      # SCH.23 Parent Placer Appointment ID
        "",                      # SCH.24 Parent Filler Appointment ID
        filler_status_code,      # SCH.25 Filler Status Code
    ]
    return "|".join(fields)
