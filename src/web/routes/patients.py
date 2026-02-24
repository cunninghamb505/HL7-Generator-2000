"""Patient API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from src.web.dependencies import deps

router = APIRouter(prefix="/api/patients", tags=["patients"])


@router.get("")
async def list_patients(
    status: str | None = None,
    limit: int = Query(default=50, le=200),
    offset: int = Query(default=0, ge=0),
):
    if not deps.patient_pool:
        return {"patients": [], "total": 0}

    patients = deps.patient_pool.list_patients(status=status, limit=limit, offset=offset)
    return {
        "patients": patients,
        "total": deps.patient_pool.total_count,
        "idle": deps.patient_pool.idle_count,
        "active": deps.patient_pool.active_count,
    }


@router.get("/{mrn}")
async def get_patient(mrn: str):
    if not deps.patient_pool:
        return {"error": "Pool not initialized"}
    patient = deps.patient_pool.get_patient(mrn)
    if not patient:
        return {"error": "Patient not found"}
    return patient.to_dict()
