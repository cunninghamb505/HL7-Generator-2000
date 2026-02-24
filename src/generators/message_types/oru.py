"""ORU (Observation Result) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.obr import build_obr
from src.generators.segment_builders.obx import build_obx
from src.generators.segment_builders.orc import build_orc
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1


class ORUGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "ORU"

    @property
    def supported_triggers(self) -> list[str]:
        return ["R01"]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        order = kwargs.get("order")
        results = kwargs.get("results", [])
        result_status = kwargs.get("result_status", "F")
        provider_id = kwargs.get("provider_id", patient.attending_doctor_id)
        provider_name = kwargs.get("provider_name", patient.attending_doctor_name)

        segments: list[str] = []

        segments.append(build_msh(
            "ORU", trigger_event, self.facility, self.hl7_version,
        ))
        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        if order:
            segments.append(build_orc(
                order,
                order_control="RE",
                ordering_provider_id=provider_id,
                ordering_provider_name=provider_name,
            ))
            segments.append(build_obr(
                order,
                ordering_provider_id=provider_id,
                ordering_provider_name=provider_name,
                result_status=result_status,
            ))

        # OBX segments for each result
        if not results and order:
            results = order.results

        for i, result in enumerate(results, 1):
            segments.append(build_obx(
                set_id=i,
                value_type=result.get("value_type", "NM"),
                observation_id=result.get("observation_id", ""),
                observation_name=result.get("observation_name", ""),
                value=result.get("value", ""),
                units=result.get("units", ""),
                reference_range=result.get("reference_range", ""),
                abnormal_flag=result.get("abnormal_flag", ""),
                result_status=result.get("result_status", result_status),
            ))

        return self._join_segments(segments)
