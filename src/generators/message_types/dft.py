"""DFT (Detailed Financial Transaction) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.ft1 import build_ft1
from src.generators.segment_builders.in1 import build_in1
from src.generators.segment_builders.in2 import build_in2
from src.generators.segment_builders.in3 import build_in3
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1


class DFTGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "DFT"

    @property
    def supported_triggers(self) -> list[str]:
        return ["P03", "P11"]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        transactions = kwargs.get("transactions", [])

        segments: list[str] = []

        segments.append(build_msh(
            "DFT", trigger_event, self.facility, self.hl7_version,
        ))
        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        # FT1 segments for each transaction
        for i, tx in enumerate(transactions, 1):
            segments.append(build_ft1(
                set_id=i,
                transaction_id=tx.get("transaction_id", ""),
                transaction_type=tx.get("transaction_type", "CG"),
                transaction_code=tx.get("transaction_code", ""),
                transaction_description=tx.get("transaction_description", ""),
                transaction_amount=tx.get("amount", ""),
                quantity=tx.get("quantity", "1"),
                department_code=tx.get("department", ""),
                diagnosis_code=tx.get("diagnosis_code", ""),
                ordering_provider=tx.get("ordering_provider", ""),
            ))

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
