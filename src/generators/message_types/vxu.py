"""VXU (Vaccination Record Update) message generator."""

from __future__ import annotations

from typing import Any

from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.obx import build_obx
from src.generators.segment_builders.orc import build_orc
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1
from src.generators.segment_builders.rxa import build_rxa


class VXUGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "VXU"

    @property
    def supported_triggers(self) -> list[str]:
        return ["V04"]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        order = kwargs.get("order")
        vaccine_code = kwargs.get("vaccine_code", "")
        vaccine_name = kwargs.get("vaccine_name", "")
        dose = kwargs.get("dose", "0.5")
        dose_units = kwargs.get("dose_units", "mL")
        route = kwargs.get("route", "IM")
        site = kwargs.get("site", "LA")  # Left Arm
        lot_number = kwargs.get("lot_number", "")
        manufacturer = kwargs.get("manufacturer", "")
        observations = kwargs.get("observations", [])

        segments: list[str] = []

        segments.append(build_msh(
            "VXU", trigger_event, self.facility, self.hl7_version,
        ))
        segments.append(build_pid(patient))
        segments.append(build_pv1(patient))

        if order:
            segments.append(build_orc(
                order,
                order_control="RE",
            ))

        segments.append(build_rxa(
            admin_code=vaccine_code,
            admin_name=vaccine_name,
            dose=dose,
            dose_units=dose_units,
            route=route,
            site=site,
            lot_number=lot_number,
            manufacturer=manufacturer,
        ))

        for i, obs in enumerate(observations, 1):
            segments.append(build_obx(
                set_id=i,
                value_type=obs.get("value_type", "CE"),
                observation_id=obs.get("observation_id", ""),
                observation_name=obs.get("observation_name", ""),
                value=obs.get("value", ""),
                result_status="F",
            ))

        return self._join_segments(segments)
