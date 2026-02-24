"""Workflow data models - definitions, steps, and types."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class StepType(str, Enum):
    REGISTRATION = "registration"
    ADMISSION = "admission"
    DISCHARGE = "discharge"
    TRANSFER = "transfer"
    LAB_ORDER = "lab_order"
    LAB_RESULT = "lab_result"
    PHARMACY_ORDER = "pharmacy_order"
    PHARMACY_DISPENSE = "pharmacy_dispense"
    VACCINATION = "vaccination"
    DOCUMENT = "document"
    BILLING = "billing"
    BAR = "bar"
    SCHEDULING = "scheduling"
    MASTER_FILE = "master_file"
    DELAY = "delay"
    CONDITION = "condition"
    REPEAT = "repeat"
    UPDATE = "update"


@dataclass
class WorkflowStep:
    step_type: StepType
    params: dict[str, Any] = field(default_factory=dict)
    # For conditions
    probability: float = 1.0
    if_true: list[WorkflowStep] = field(default_factory=list)
    if_false: list[WorkflowStep] = field(default_factory=list)
    # For repeats
    repeat_count: int = 1
    repeat_steps: list[WorkflowStep] = field(default_factory=list)
    repeat_delay: str = ""


@dataclass
class WorkflowDefinition:
    name: str
    description: str = ""
    weight: float = 1.0
    patient_class: str = ""
    steps: list[WorkflowStep] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "patient_class": self.patient_class,
            "steps_count": len(self.steps),
            "tags": self.tags,
        }
