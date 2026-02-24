"""ORM (Order) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.obr import build_obr
from src.generators.segment_builders.orc import build_orc
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1


class ORMGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "ORM"

    @property
    def supported_triggers(self) -> list[str]:
        return ["O01"]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        order = kwargs.get("order")
        order_control = kwargs.get("order_control", "NW")
        provider_id = kwargs.get("provider_id", patient.attending_doctor_id)
        provider_name = kwargs.get("provider_name", patient.attending_doctor_name)

        segments: list[str] = []

        segments.append(build_msh(
            "ORM", trigger_event, self.facility, self.hl7_version,
        ))
        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        if order:
            segments.append(build_orc(
                order,
                order_control=order_control,
                ordering_provider_id=provider_id,
                ordering_provider_name=provider_name,
            ))
            segments.append(build_obr(
                order,
                ordering_provider_id=provider_id,
                ordering_provider_name=provider_name,
            ))

        return self._join_segments(segments)
