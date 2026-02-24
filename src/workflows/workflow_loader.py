"""YAML workflow loader - parses workflow YAML files into WorkflowDefinition objects."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.workflows.workflow_models import WorkflowDefinition, WorkflowStep, StepType


def _parse_step(raw: dict[str, Any] | str) -> WorkflowStep:
    """Parse a single step from YAML."""
    if isinstance(raw, str):
        # Simple step like "discharge" with no params
        return WorkflowStep(step_type=StepType(raw))

    # Should be a single-key dict
    for key, value in raw.items():
        if key == "delay":
            return WorkflowStep(
                step_type=StepType.DELAY,
                params=value if isinstance(value, dict) else {"duration": value},
            )
        elif key == "condition":
            cond = value if isinstance(value, dict) else {}
            step = WorkflowStep(
                step_type=StepType.CONDITION,
                probability=cond.get("probability", 0.5),
            )
            if "if_true" in cond:
                step.if_true = [_parse_step(s) for s in cond["if_true"]]
            if "if_false" in cond:
                step.if_false = [_parse_step(s) for s in cond["if_false"]]
            return step
        elif key == "repeat":
            rep = value if isinstance(value, dict) else {}
            step = WorkflowStep(
                step_type=StepType.REPEAT,
                repeat_count=rep.get("count", 1),
                repeat_delay=rep.get("delay", ""),
            )
            if "steps" in rep:
                step.repeat_steps = [_parse_step(s) for s in rep["steps"]]
            return step
        else:
            # Regular step type with params
            try:
                step_type = StepType(key)
            except ValueError:
                step_type = StepType(key)
            params = value if isinstance(value, dict) else {}
            return WorkflowStep(step_type=step_type, params=params)

    return WorkflowStep(step_type=StepType.DELAY)


def load_workflow(filepath: str | Path) -> WorkflowDefinition:
    """Load a single workflow from a YAML file."""
    filepath = Path(filepath)
    with open(filepath) as f:
        raw = yaml.safe_load(f) or {}

    steps = [_parse_step(s) for s in raw.get("steps", [])]

    return WorkflowDefinition(
        name=raw.get("name", filepath.stem),
        description=raw.get("description", ""),
        weight=raw.get("weight", 1.0),
        patient_class=raw.get("patient_class", ""),
        steps=steps,
        tags=raw.get("tags", []),
    )


def load_workflows_from_dir(directory: str | Path) -> list[WorkflowDefinition]:
    """Load all workflow YAML files from a directory."""
    directory = Path(directory)
    workflows: list[WorkflowDefinition] = []
    if not directory.exists():
        return workflows

    for filepath in sorted(directory.glob("*.yaml")):
        try:
            workflow = load_workflow(filepath)
            workflows.append(workflow)
        except Exception as e:
            import structlog
            logger = structlog.get_logger(__name__)
            logger.error("workflow_load_failed", file=str(filepath), error=str(e))

    return workflows
