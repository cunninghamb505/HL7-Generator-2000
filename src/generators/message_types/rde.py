"""RDE (Pharmacy/Treatment Encoded Order) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.orc import build_orc
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1
from src.generators.segment_builders.rxe import build_rxe


class RDEGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "RDE"

    @property
    def supported_triggers(self) -> list[str]:
        return ["O11", "O25"]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        order = kwargs.get("order")
        drug_code = kwargs.get("drug_code", "")
        drug_name = kwargs.get("drug_name", "")
        dose = kwargs.get("dose", "")
        dose_units = kwargs.get("dose_units", "mg")
        route = kwargs.get("route", "PO")
        frequency = kwargs.get("frequency", "")
        quantity = kwargs.get("quantity", "")
        order_control = kwargs.get("order_control", "NW")

        segments: list[str] = []

        segments.append(build_msh(
            "RDE", trigger_event, self.facility, self.hl7_version,
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

        segments.append(build_rxe(
            drug_code=drug_code,
            drug_name=drug_name,
            dose=dose,
            dose_units=dose_units,
            route=route,
            frequency=frequency,
            quantity=quantity,
        ))

        return self._join_segments(segments)
