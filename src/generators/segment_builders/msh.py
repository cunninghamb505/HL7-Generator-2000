"""MSH (Message Header) segment builder."""

from __future__ import annotations

from datetime import datetime

from src.core.config import FacilityConfig
from src.data.identifiers import generate_message_control_id
from src.utils.hl7_helpers import format_timestamp


def build_msh(
    message_type: str,
    trigger_event: str,
    facility: FacilityConfig,
    hl7_version: str = "2.5.1",
    processing_id: str = "P",
    message_control_id: str = "",
    timestamp: datetime | None = None,
) -> str:
    """Build MSH segment string.

    Returns: MSH|^~\\&|sending_app|sending_fac|recv_app|recv_fac|timestamp||MSG^TRG|ctrl_id|P|version
    """
    if not message_control_id:
        message_control_id = generate_message_control_id()

    ts = format_timestamp(timestamp)
    msg_type = f"{message_type}^{trigger_event}"

    fields = [
        "MSH",
        "^~\\&",
        facility.sending_application,
        facility.sending_facility,
        facility.receiving_application,
        facility.receiving_facility,
        ts,
        "",  # Security
        msg_type,
        message_control_id,
        processing_id,
        hl7_version,
    ]
    return "|".join(fields)
