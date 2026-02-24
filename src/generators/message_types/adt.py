"""ADT (Admit/Discharge/Transfer) message generator.

Supports A01-A40+ trigger events covering admit, discharge, transfer,
registration, merge, swap, and more.
"""

from __future__ import annotations

from typing import Any

from src.core.config import FacilityConfig
from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.segment_builders.al1 import build_al1_segments
from src.generators.segment_builders.dg1 import build_dg1_segments
from src.generators.segment_builders.evn import build_evn
from src.generators.segment_builders.in1 import build_in1
from src.generators.segment_builders.in2 import build_in2
from src.generators.segment_builders.in3 import build_in3
from src.generators.segment_builders.mrg import build_mrg
from src.generators.segment_builders.msh import build_msh
from src.generators.segment_builders.nk1 import build_nk1
from src.generators.segment_builders.pid import build_pid
from src.generators.segment_builders.pv1 import build_pv1
from src.generators.segment_builders.pv2 import build_pv2


class ADTGenerator(MessageGenerator):
    @property
    def message_type(self) -> str:
        return "ADT"

    @property
    def supported_triggers(self) -> list[str]:
        return [
            "A01",  # Admit/Visit Notification
            "A02",  # Transfer a Patient
            "A03",  # Discharge/End Visit
            "A04",  # Register a Patient
            "A05",  # Pre-Admit a Patient
            "A06",  # Change Outpatient to Inpatient
            "A07",  # Change Inpatient to Outpatient
            "A08",  # Update Patient Information
            "A09",  # Patient Departing - Tracking
            "A10",  # Patient Arriving - Tracking
            "A11",  # Cancel Admit
            "A12",  # Cancel Transfer
            "A13",  # Cancel Discharge
            "A14",  # Pending Admit
            "A15",  # Pending Transfer
            "A16",  # Pending Discharge
            "A17",  # Swap Patients
            "A18",  # Merge Patient Information
            "A23",  # Delete a Patient Record
            "A25",  # Cancel Pending Discharge
            "A26",  # Cancel Pending Transfer
            "A27",  # Cancel Pending Admit
            "A28",  # Add Person Information
            "A29",  # Delete Person Information
            "A31",  # Update Person Information
            "A34",  # Merge Patient Info - Patient ID Only
            "A35",  # Merge Patient Info - Account Number Only
            "A36",  # Merge Patient Info - Patient ID & Account
            "A40",  # Merge Patient - Patient Identifier List
        ]

    def generate(
        self,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        segments: list[str] = []

        # MSH
        segments.append(build_msh(
            "ADT", trigger_event, self.facility, self.hl7_version,
        ))

        # EVN
        segments.append(build_evn(trigger_event))

        # PID
        segments.append(build_pid(patient))

        # NK1 (if available)
        nk1 = build_nk1(patient)
        if nk1:
            segments.append(nk1)

        # PV1
        segments.append(build_pv1(patient))

        # PV2 for certain events
        if trigger_event in ("A01", "A02", "A05", "A06", "A07", "A14", "A15"):
            segments.append(build_pv2(
                patient,
                admit_reason=kwargs.get("admit_reason", ""),
                transfer_reason=kwargs.get("transfer_reason", ""),
            ))

        # AL1 segments
        if patient.allergies:
            segments.extend(build_al1_segments(patient.allergies))

        # DG1 segments
        if patient.diagnoses:
            segments.extend(build_dg1_segments(patient.diagnoses))

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

        # MRG for merge events
        if trigger_event in ("A17", "A18", "A34", "A35", "A36", "A40"):
            prior_mrn = kwargs.get("prior_mrn", "")
            prior_account = kwargs.get("prior_account", "")
            prior_name = kwargs.get("prior_name", "")
            if prior_mrn:
                segments.append(build_mrg(prior_mrn, prior_account, prior_name=prior_name))

        return self._join_segments(segments)
