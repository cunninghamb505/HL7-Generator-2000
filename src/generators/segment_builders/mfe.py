"""MFE (Master File Entry) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_mfe(
    record_level_event_code: str = "MAD",
    mfn_control_id: str = "",
    effective_datetime: datetime | None = None,
    primary_key_value: str = "",
    primary_key_type: str = "CE",
) -> str:
    """Build MFE segment.

    record_level_event_code: MAD=Add, MDL=Delete, MUP=Update, MDC=Deactivate, MAC=Reactivate
    """
    effective = format_timestamp(effective_datetime) if effective_datetime else ""

    fields = [
        "MFE",
        record_level_event_code,  # MFE.1 Record-Level Event Code
        mfn_control_id,           # MFE.2 MFN Control ID
        effective,                # MFE.3 Effective Date/Time
        primary_key_value,        # MFE.4 Primary Key Value - MFE
        primary_key_type,         # MFE.5 Primary Key Value Type
    ]
    return "|".join(fields)
