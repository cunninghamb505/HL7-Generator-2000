"""Workflow API routes."""

from __future__ import annotations

from fastapi import APIRouter

from src.web.dependencies import deps

router = APIRouter(prefix="/api/workflows", tags=["workflows"])


@router.get("")
async def list_workflows():
    if not deps.workflow_registry:
        return {"workflows": []}
    return {"workflows": deps.workflow_registry.list_all()}


@router.post("/{workflow_name}/trigger")
async def trigger_workflow(workflow_name: str):
    if not deps.engine:
        return {"error": "Engine not initialized"}
    result = await deps.engine.trigger_workflow(workflow_name)
    return result
