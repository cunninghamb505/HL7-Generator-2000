"""TXA (Transcription Document Header) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.utils.hl7_helpers import format_timestamp


def build_txa(
    set_id: int = 1,
    document_type: str = "HP",
    document_content_presentation: str = "TX",
    activity_datetime: datetime | None = None,
    originator: str = "",
    unique_document_number: str = "",
    document_completion_status: str = "AU",
    document_availability_status: str = "AV",
) -> str:
    """Build TXA segment for document messages.

    document_type: HP=History & Physical, DS=Discharge Summary, CN=Consult Note, etc.
    document_completion_status: DO=Dictated, IP=In Progress, AU=Authenticated, LA=Legally Auth
    """
    ts = format_timestamp(activity_datetime)

    fields = [
        "TXA",
        str(set_id),                           # TXA.1 Set ID
        document_type,                          # TXA.2 Document Type
        document_content_presentation,          # TXA.3 Document Content Presentation
        ts,                                     # TXA.4 Activity Date/Time
        "",                                     # TXA.5 Primary Activity Provider Code
        "",                                     # TXA.6 Origination Date/Time
        "",                                     # TXA.7 Transcription Date/Time
        "",                                     # TXA.8 Edit Date/Time
        originator,                             # TXA.9 Originator Code/Name
        "",                                     # TXA.10 Assigned Document Authenticator
        "",                                     # TXA.11 Transcriptionist Code/Name
        unique_document_number,                 # TXA.12 Unique Document Number
        "",                                     # TXA.13 Parent Document Number
        "",                                     # TXA.14 Placer Order Number
        "",                                     # TXA.15 Filler Order Number
        "",                                     # TXA.16 Unique Document File Name
        document_completion_status,             # TXA.17 Document Completion Status
        "",                                     # TXA.18 Document Confidentiality Status
        document_availability_status,           # TXA.19 Document Availability Status
    ]
    return "|".join(fields)
