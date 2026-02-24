"""ACK (Acknowledgment) message generator."""

from __future__ import annotations

from typing import Any

from src.core.config import FacilityConfig
from src.core.patient import Patient
from src.data.identifiers import generate_message_control_id
from src.generators.base import MessageGenerator
from src.generators.segment_builders.msh import build_msh
from src.utils.hl7_helpers import format_timestamp


class ACKGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "ACK"

    @property
    def supported_triggers(self) -> list[str]:
        return [""]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        return self.generate_ack(**kwargs)

    def generate_ack(
        self,
        ack_code: str = "AA",
        message_control_id: str = "",
        text_message: str = "",
        error_code: str = "",
        **_: Any,
    ) -> str:
        """Generate an ACK message.

        ack_code: AA=Accept, AE=Application Error, AR=Application Reject
        """
        segments: list[str] = []

        segments.append(build_msh(
            "ACK", "", self.facility, self.hl7_version,
        ))

        # MSA segment
        msa_fields = [
            "MSA",
            ack_code,
            message_control_id,
            text_message,
        ]
        segments.append("|".join(msa_fields))

        # ERR segment for error responses
        if ack_code in ("AE", "AR") and error_code:
            err_fields = [
                "ERR",
                error_code,
            ]
            segments.append("|".join(err_fields))

        return "\r".join(segments)
