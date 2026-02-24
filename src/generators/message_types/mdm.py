"""MDM (Medical Document Management) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.obx import build_obx
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1
from src.generators.segment_builders.txa import build_txa


class MDMGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "MDM"

    @property
    def supported_triggers(self) -> list[str]:
        return [
            "T01",  # Original document notification
            "T02",  # Original document notification and content
            "T03",  # Document status change notification
            "T04",  # Document status change notification and content
            "T05",  # Document addendum notification
            "T06",  # Document addendum notification and content
            "T07",  # Document edit notification
            "T08",  # Document edit notification and content
            "T09",  # Document replacement notification
            "T10",  # Document replacement notification and content
            "T11",  # Document cancel notification
        ]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        document_type = kwargs.get("document_type", "HP")
        document_id = kwargs.get("document_id", "")
        document_text = kwargs.get("document_text", "")
        completion_status = kwargs.get("completion_status", "AU")
        originator = kwargs.get("originator", "")

        if not originator and patient.attending_doctor_id:
            originator = f"{patient.attending_doctor_id}^{patient.attending_doctor_name}"

        segments: list[str] = []

        segments.append(build_msh(
            "MDM", trigger_event, self.facility, self.hl7_version,
        ))

        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        segments.append(build_txa(
            document_type=document_type,
            originator=originator,
            unique_document_number=document_id,
            document_completion_status=completion_status,
        ))

        # Include document content for even-numbered triggers
        if trigger_event in ("T02", "T04", "T06", "T08", "T10") and document_text:
            segments.append(build_obx(
                set_id=1,
                value_type="TX",
                observation_id="",
                observation_name="Document Text",
                value=document_text,
                result_status="F",
            ))

        return self._join_segments(segments)
