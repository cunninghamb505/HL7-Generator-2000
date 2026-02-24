"""SIU (Scheduling Information Unsolicited) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.aig import build_aig
from src.generators.segment_builders.ail import build_ail
from src.generators.segment_builders.aip import build_aip
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1
from src.generators.segment_builders.sch import build_sch


class SIUGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "SIU"

    @property
    def supported_triggers(self) -> list[str]:
        return [
            "S12",  # New appointment booking
            "S13",  # Appointment rescheduling
            "S14",  # Appointment modification
            "S15",  # Appointment cancellation
            "S16",  # Appointment discontinue
            "S17",  # Appointment deletion
            "S26",  # Appointment no-show
        ]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        appointment_id = kwargs.get("appointment_id", "")
        appointment_type = kwargs.get("appointment_type", "ROUTINE")
        appointment_reason = kwargs.get("appointment_reason", "")
        duration = kwargs.get("duration", "30")
        start_datetime = kwargs.get("start_datetime")
        end_datetime = kwargs.get("end_datetime")
        location = kwargs.get("location", patient.location)
        provider_id = kwargs.get("provider_id", patient.attending_doctor_id)
        provider_name = kwargs.get("provider_name", patient.attending_doctor_name)
        filler_status = kwargs.get("filler_status", "Booked")

        segments: list[str] = []

        segments.append(build_msh(
            "SIU", trigger_event, self.facility, self.hl7_version,
        ))

        segments.append(build_sch(
            placer_appointment_id=appointment_id,
            filler_appointment_id=appointment_id,
            event_reason=appointment_reason,
            appointment_type=appointment_type,
            appointment_duration=duration,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            filler_status_code=filler_status,
        ))

        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        # Resource segments
        if location:
            segments.append(build_ail(
                location_resource_id=location,
                start_datetime=start_datetime,
                duration=duration,
            ))

        if provider_id:
            segments.append(build_aip(
                resource_id=provider_id,
                resource_name=provider_name,
                start_datetime=start_datetime,
                duration=duration,
            ))

        segments.append(build_aig(
            resource_id=appointment_type,
            start_datetime=start_datetime,
            duration=duration,
        ))

        return self._join_segments(segments)
