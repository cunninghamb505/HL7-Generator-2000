"""Control API routes - start, stop, pause the simulation."""

from __future__ import annotations

from fastapi import APIRouter

from src.web.dependencies import deps

router = APIRouter(prefix="/api/control", tags=["control"])


@router.post("/start")
async def start_simulation():
    if deps.engine:
        await deps.engine.start()
    return {"status": "started"}


@router.post("/stop")
async def stop_simulation():
    if deps.engine:
        await deps.engine.stop()
    return {"status": "stopped"}


@router.post("/pause")
async def pause_simulation():
    if deps.engine:
        await deps.engine.pause()
    return {"status": "paused"}


@router.post("/resume")
async def resume_simulation():
    if deps.engine:
        await deps.engine.resume()
    return {"status": "resumed"}


@router.post("/rate")
async def set_rate(rate: float):
    if deps.engine:
        deps.engine.set_rate(rate)
    return {"rate": rate}
