"""MFI (Master File Identification) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_mfi(
    master_file_identifier: str,
    master_file_application_id: str = "",
    file_level_event_code: str = "UPD",
    entered_datetime: datetime | None = None,
    effective_datetime: datetime | None = None,
    response_level_code: str = "NE",
) -> str:
    """Build MFI segment.

    file_level_event_code: REP=Replace, UPD=Update, DEL=Delete
    response_level_code: NE=Never, ER=Error only, AL=Always, SU=Success only
    """
    entered = format_timestamp(entered_datetime)
    effective = format_timestamp(effective_datetime) if effective_datetime else ""

    fields = [
        "MFI",
        master_file_identifier,       # MFI.1 Master File Identifier
        master_file_application_id,   # MFI.2 Master File Application Identifier
        file_level_event_code,        # MFI.3 File-Level Event Code
        entered,                      # MFI.4 Entered Date/Time
        effective,                    # MFI.5 Effective Date/Time
        response_level_code,          # MFI.6 Response Level Code
    ]
    return "|".join(fields)
