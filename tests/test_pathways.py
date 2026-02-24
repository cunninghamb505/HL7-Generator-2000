"""Tests for workflow loading and models."""

from pathlib import Path

from src.workflows.workflow_loader import load_workflow, load_workflows_from_dir
from src.workflows.workflow_models import StepType
from src.workflows.workflow_registry import WorkflowRegistry


def test_load_er_workflow():
    wf = load_workflow("config/workflows/er_visit_with_labs.yaml")
    assert wf.name == "er_visit_with_labs"
    assert wf.weight == 3.0
    assert len(wf.steps) > 0
    assert wf.steps[0].step_type == StepType.REGISTRATION


def test_load_inpatient_workflow():
    wf = load_workflow("config/workflows/inpatient_admission.yaml")
    assert wf.name == "inpatient_admission"
    assert len(wf.steps) > 5


def test_load_all_workflows():
    workflows = load_workflows_from_dir("config/workflows")
    assert len(workflows) >= 10  # We have 12 workflow files


def test_workflow_registry():
    registry = WorkflowRegistry()
    count = registry.load_from_directory("config/workflows")
    assert count >= 10
    assert registry.count == count

    # Test pick random
    wf = registry.pick_random()
    assert wf is not None
    assert wf.name in registry.names

    # Test get
    er = registry.get("er_visit_with_labs")
    assert er is not None
    assert er.name == "er_visit_with_labs"


def test_workflow_conditions():
    wf = load_workflow("config/workflows/er_visit_with_labs.yaml")
    # Find a condition step
    condition_steps = [s for s in wf.steps if s.step_type == StepType.CONDITION]
    assert len(condition_steps) > 0
    cond = condition_steps[0]
    assert 0 < cond.probability <= 1.0
    assert len(cond.if_true) > 0


def test_workflow_delays():
    wf = load_workflow("config/workflows/er_visit_with_labs.yaml")
    delay_steps = [s for s in wf.steps if s.step_type == StepType.DELAY]
    assert len(delay_steps) > 0
    d = delay_steps[0]
    assert "min" in d.params or "duration" in d.params


def test_workflow_to_dict():
    wf = load_workflow("config/workflows/er_visit_with_labs.yaml")
    d = wf.to_dict()
    assert d["name"] == "er_visit_with_labs"
    assert "steps_count" in d
    assert d["steps_count"] > 0
