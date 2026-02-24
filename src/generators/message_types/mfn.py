"""MFN (Master File Notification) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.mfe import build_mfe
from src.generators.segment_builders.mfi import build_mfi
from src.generators.segment_builders.msh import build_msh


class MFNGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "MFN"

    @property
    def supported_triggers(self) -> list[str]:
        return [
            "M01",  # Master File Not Otherwise Specified
            "M02",  # Staff/Practitioner
            "M04",  # Charge Description
            "M05",  # Patient Location
            "M08",  # Test/Observation (Numeric)
            "M09",  # Test/Observation (Categorical)
            "M10",  # Test/Observation Batteries
            "M13",  # Master File - General
        ]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        master_file_id = kwargs.get("master_file_id", "")
        entries = kwargs.get("entries", [])
        event_code = kwargs.get("event_code", "UPD")

        segments: list[str] = []

        segments.append(build_msh(
            "MFN", trigger_event, self.facility, self.hl7_version,
        ))

        segments.append(build_mfi(
            master_file_identifier=master_file_id,
            file_level_event_code=event_code,
        ))

        for entry in entries:
            segments.append(build_mfe(
                record_level_event_code=entry.get("event_code", "MAD"),
                mfn_control_id=entry.get("control_id", ""),
                primary_key_value=entry.get("primary_key", ""),
            ))

        return self._join_segments(segments)
