"""Metrics API routes."""

from __future__ import annotations

from fastapi import APIRouter

from src.web.dependencies import deps

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("")
async def get_metrics():
    result = {}

    if deps.state:
        result.update(deps.state.to_dict())

    if deps.patient_pool:
        result["patients_total"] = deps.patient_pool.total_count
        result["patients_idle"] = deps.patient_pool.idle_count
        result["patients_active"] = deps.patient_pool.active_count

    if deps.message_log:
        result["messages_logged"] = deps.message_log.total_count

    if deps.ws_manager:
        result["ws_connections"] = deps.ws_manager.connection_count

    if deps.workflow_registry:
        result["workflows_loaded"] = deps.workflow_registry.count

    if deps.message_factory:
        result["generators"] = deps.message_factory.supported_types

    return result
