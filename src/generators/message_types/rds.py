"""RDS (Pharmacy/Treatment Dispense) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.orc import build_orc
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1
from src.generators.segment_builders.rxd import build_rxd


class RDSGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "RDS"

    @property
    def supported_triggers(self) -> list[str]:
        return ["O13"]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        order = kwargs.get("order")
        drug_code = kwargs.get("drug_code", "")
        drug_name = kwargs.get("drug_name", "")
        quantity = kwargs.get("quantity", "1")
        units = kwargs.get("units", "")
        prescription_number = kwargs.get("prescription_number", "")
        order_control = kwargs.get("order_control", "RE")

        segments: list[str] = []

        segments.append(build_msh(
            "RDS", trigger_event, self.facility, self.hl7_version,
        ))
        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        if order:
            segments.append(build_orc(
                order,
                order_control=order_control,
                ordering_provider_id=patient.attending_doctor_id,
                ordering_provider_name=patient.attending_doctor_name,
            ))

        segments.append(build_rxd(
            dispense_code=drug_code,
            dispense_name=drug_name,
            actual_quantity=quantity,
            actual_units=units,
            prescription_number=prescription_number,
        ))

        return self._join_segments(segments)
