"""Async workflow executor with delay, condition, and repeat support."""

from __future__ import annotations

import asyncio
import random
import re
from typing import Any

import structlog

from src.core.clock import SimulationClock
from src.core.patient import Patient
from src.core.state import SimulationState
from src.generators.message_factory import MessageFactory
from src.workflows.workflow_models import WorkflowDefinition, WorkflowStep, StepType
from src.workflows.step_handlers.base import Event, get_handler
from src.transport.message_router import MessageRouter

logger = structlog.get_logger(__name__)


def _parse_duration(duration_str: str) -> float:
    """Parse a duration string like '5m', '2h', '30s' to seconds."""
    if not duration_str:
        return 0

    match = re.match(r"(\d+(?:\.\d+)?)\s*(s|m|h|d)?", str(duration_str).strip())
    if not match:
        try:
            return float(duration_str)
        except (ValueError, TypeError):
            return 0

    value = float(match.group(1))
    unit = match.group(2) or "s"

    multipliers = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    return value * multipliers.get(unit, 1)


class WorkflowEngine:
    def __init__(
        self,
        message_factory: MessageFactory,
        message_router: MessageRouter,
        clock: SimulationClock,
        state: SimulationState,
    ):
        self._factory = message_factory
        self._router = message_router
        self._clock = clock
        self._state = state

    async def execute_workflow(
        self,
        workflow: WorkflowDefinition,
        patient: Patient,
    ) -> None:
        """Execute a complete workflow for a patient."""
        patient.active_workflow = workflow.name
        patient.workflow_step = 0
        self._state.active_workflows += 1

        logger.info(
            "workflow_started",
            workflow=workflow.name,
            patient=patient.mrn,
        )

        try:
            await self._execute_steps(workflow.steps, patient)
        except asyncio.CancelledError:
            logger.info("workflow_cancelled", workflow=workflow.name, patient=patient.mrn)
        except Exception as e:
            logger.error(
                "workflow_error",
                workflow=workflow.name,
                patient=patient.mrn,
                error=str(e),
            )
            self._state.record_error()
        finally:
            self._state.active_workflows = max(0, self._state.active_workflows - 1)
            self._state.completed_workflows += 1
            patient.active_workflow = ""

        logger.info(
            "workflow_completed",
            workflow=workflow.name,
            patient=patient.mrn,
        )

    async def _execute_steps(
        self, steps: list[WorkflowStep], patient: Patient,
    ) -> None:
        """Execute a list of steps sequentially."""
        for step in steps:
            patient.workflow_step += 1

            if step.step_type == StepType.DELAY:
                await self._handle_delay(step)
            elif step.step_type == StepType.CONDITION:
                await self._handle_condition(step, patient)
            elif step.step_type == StepType.REPEAT:
                await self._handle_repeat(step, patient)
            else:
                await self._handle_step(step, patient)

    async def _handle_step(self, step: WorkflowStep, patient: Patient) -> None:
        """Handle a regular step: get handler, produce events, generate & route messages."""
        handler = get_handler(step.step_type.value)
        if not handler:
            logger.warning("no_handler", step_type=step.step_type.value)
            return

        events = handler.handle(patient, step.params)

        for event in events:
            try:
                message = self._factory.generate(
                    event.message_type,
                    event.trigger_event,
                    event.patient,
                    **event.kwargs,
                )

                await self._router.route(
                    message,
                    event.patient,
                    message_type=event.message_type,
                    trigger_event=event.trigger_event,
                )

                self._state.record_message(
                    f"{event.message_type}^{event.trigger_event}"
                )
            except Exception as e:
                logger.error(
                    "message_generation_error",
                    message_type=event.message_type,
                    error=str(e),
                )
                self._state.record_error()

    async def _handle_delay(self, step: WorkflowStep) -> None:
        """Handle a delay step with min/max range."""
        params = step.params
        min_delay = _parse_duration(str(params.get("min", params.get("duration", "1s"))))
        max_delay = _parse_duration(str(params.get("max", min_delay)))

        if max_delay < min_delay:
            max_delay = min_delay

        delay = random.uniform(min_delay, max_delay)

        logger.debug("workflow_delay", seconds=round(delay, 1))
        await self._clock.sleep(delay)

    async def _handle_condition(self, step: WorkflowStep, patient: Patient) -> None:
        """Handle a condition step with probability branching."""
        if random.random() < step.probability:
            if step.if_true:
                await self._execute_steps(step.if_true, patient)
        else:
            if step.if_false:
                await self._execute_steps(step.if_false, patient)

    async def _handle_repeat(self, step: WorkflowStep, patient: Patient) -> None:
        """Handle a repeat step."""
        delay_seconds = _parse_duration(step.repeat_delay) if step.repeat_delay else 0

        for i in range(step.repeat_count):
            if step.repeat_steps:
                await self._execute_steps(step.repeat_steps, patient)
            if delay_seconds > 0 and i < step.repeat_count - 1:
                await self._clock.sleep(delay_seconds)
