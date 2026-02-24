"""BAR (Billing Account Record) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.dg1 import build_dg1_segments
from src.generators.segment_builders.evn import build_evn
from src.generators.segment_builders.gt1 import build_gt1
from src.generators.segment_builders.in1 import build_in1
from src.generators.segment_builders.in2 import build_in2
from src.generators.segment_builders.in3 import build_in3
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1


class BARGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "BAR"

    @property
    def supported_triggers(self) -> list[str]:
        return ["P01", "P02", "P05", "P06"]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        segments: list[str] = []

        segments.append(build_msh(
            "BAR", trigger_event, self.facility, self.hl7_version,
        ))
        segments.append(build_evn(trigger_event))
        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        # DG1
        if patient.diagnoses:
            segments.extend(build_dg1_segments(patient.diagnoses))

        # GT1
        segments.append(build_gt1(patient))

        # IN1 / IN2 / IN3 (insurance)
        in1 = build_in1(patient)
        if in1:
            segments.append(in1)
            in2 = build_in2(patient)
            if in2:
                segments.append(in2)
            in3 = build_in3(patient)
            if in3:
                segments.append(in3)

        return self._join_segments(segments)
