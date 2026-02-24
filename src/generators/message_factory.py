"""Routes events to the correct message generator."""

from __future__ import annotations

from typing import Any

from src.core.config import FacilityConfig
from src.core.patient import Patient
from src.generators.base import MessageGenerator
from src.generators.message_types.ack import ACKGenerator
from src.generators.message_types.adt import ADTGenerator
from src.generators.message_types.bar import BARGenerator
from src.generators.message_types.dft import DFTGenerator
from src.generators.message_types.mdm import MDMGenerator
from src.generators.message_types.mfn import MFNGenerator
from src.generators.message_types.orm import ORMGenerator
from src.generators.message_types.oru import ORUGenerator
from src.generators.message_types.rde import RDEGenerator
from src.generators.message_types.rds import RDSGenerator
from src.generators.message_types.siu import SIUGenerator
from src.generators.message_types.vxu import VXUGenerator


class MessageFactory:
    def __init__(self, facility: FacilityConfig, hl7_version: str = "2.5.1"):
        self._generators: dict[str, MessageGenerator] = {}
        self._facility = facility
        self._hl7_version = hl7_version
        self._register_defaults()

    def _register_defaults(self) -> None:
        generator_classes = [
            ADTGenerator, ORMGenerator, ORUGenerator,
            RDEGenerator, RDSGenerator, MDMGenerator,
            DFTGenerator, VXUGenerator, BARGenerator,
            SIUGenerator, MFNGenerator, ACKGenerator,
        ]
        for cls in generator_classes:
            gen = cls(self._facility, self._hl7_version)
            self._generators[gen.message_type] = gen

    def get_generator(self, message_type: str) -> MessageGenerator | None:
        return self._generators.get(message_type.upper())

    def generate(
        self,
        message_type: str,
        trigger_event: str,
        patient: Patient,
        **kwargs: Any,
    ) -> str:
        gen = self.get_generator(message_type)
        if not gen:
            raise ValueError(f"Unknown message type: {message_type}")
        return gen.generate(trigger_event, patient, **kwargs)

    @property
    def supported_types(self) -> list[str]:
        return sorted(self._generators.keys())

    def list_generators(self) -> list[dict[str, Any]]:
        result = []
        for name, gen in sorted(self._generators.items()):
            result.append({
                "message_type": name,
                "triggers": gen.supported_triggers,
            })
        return result
