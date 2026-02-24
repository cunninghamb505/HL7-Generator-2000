"""Registry of loaded workflow definitions."""

from __future__ import annotations

import random
from typing import Any

from src.workflows.workflow_loader import load_workflows_from_dir
from src.workflows.workflow_models import WorkflowDefinition


class WorkflowRegistry:
    def __init__(self) -> None:
        self._workflows: dict[str, WorkflowDefinition] = {}

    def load_from_directory(self, directory: str) -> int:
        """Load all workflows from a directory. Returns count loaded."""
        workflows = load_workflows_from_dir(directory)
        for wf in workflows:
            self._workflows[wf.name] = wf
        return len(workflows)

    def register(self, workflow: WorkflowDefinition) -> None:
        self._workflows[workflow.name] = workflow

    def get(self, name: str) -> WorkflowDefinition | None:
        return self._workflows.get(name)

    def pick_random(self) -> WorkflowDefinition | None:
        """Pick a random workflow weighted by workflow weight."""
        if not self._workflows:
            return None
        workflows = list(self._workflows.values())
        weights = [wf.weight for wf in workflows]
        return random.choices(workflows, weights=weights, k=1)[0]

    def list_all(self) -> list[dict[str, Any]]:
        return [wf.to_dict() for wf in self._workflows.values()]

    @property
    def count(self) -> int:
        return len(self._workflows)

    @property
    def names(self) -> list[str]:
        return list(self._workflows.keys())
