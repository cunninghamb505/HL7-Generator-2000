"""Step handler base class and event model."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from src.core.patient import Patient


@dataclass
class Event:
    """An event produced by a step handler, to be turned into an HL7 message."""
    message_type: str
    trigger_event: str
    patient: Patient
    kwargs: dict[str, Any] = field(default_factory=dict)


class StepHandler(ABC):
    """Base class for workflow step handlers."""

    @abstractmethod
    def handle(self, patient: Patient, params: dict[str, Any]) -> list[Event]:
        """Process a step, mutate patient state, return events."""
        ...


# Registry of step handlers by step type name
_handler_registry: dict[str, StepHandler] = {}


def register_handler(step_type: str, handler: StepHandler) -> None:
    _handler_registry[step_type] = handler


def get_handler(step_type: str) -> StepHandler | None:
    return _handler_registry.get(step_type)


def init_handlers() -> None:
    """Initialize and register all built-in step handlers."""
    from src.workflows.step_handlers.admission import AdmissionHandler
    from src.workflows.step_handlers.bar import BARHandler
    from src.workflows.step_handlers.billing import BillingHandler
    from src.workflows.step_handlers.discharge import DischargeHandler
    from src.workflows.step_handlers.document import DocumentHandler
    from src.workflows.step_handlers.lab_order import LabOrderHandler
    from src.workflows.step_handlers.lab_result import LabResultHandler
    from src.workflows.step_handlers.master_file import MasterFileHandler
    from src.workflows.step_handlers.pharmacy_dispense import PharmacyDispenseHandler
    from src.workflows.step_handlers.pharmacy_order import PharmacyOrderHandler
    from src.workflows.step_handlers.scheduling import SchedulingHandler
    from src.workflows.step_handlers.transfer import TransferHandler
    from src.workflows.step_handlers.vaccination import VaccinationHandler

    register_handler("registration", AdmissionHandler())
    register_handler("admission", AdmissionHandler())
    register_handler("discharge", DischargeHandler())
    register_handler("transfer", TransferHandler())
    register_handler("lab_order", LabOrderHandler())
    register_handler("lab_result", LabResultHandler())
    register_handler("pharmacy_order", PharmacyOrderHandler())
    register_handler("pharmacy_dispense", PharmacyDispenseHandler())
    register_handler("vaccination", VaccinationHandler())
    register_handler("document", DocumentHandler())
    register_handler("billing", BillingHandler())
    register_handler("bar", BARHandler())
    register_handler("scheduling", SchedulingHandler())
    register_handler("master_file", MasterFileHandler())
