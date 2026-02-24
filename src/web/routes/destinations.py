"""Destination management API routes."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel

from src.core.config import DestinationConfig
from src.web.dependencies import deps

router = APIRouter(prefix="/api/destinations", tags=["destinations"])


class DestinationCreate(BaseModel):
    name: str
    type: str = "mllp"
    host: str = "127.0.0.1"
    port: int = 2575
    enabled: bool = True
    file_path: str = ""


class DestinationUpdate(BaseModel):
    enabled: bool | None = None
    host: str | None = None
    port: int | None = None


@router.get("")
async def list_destinations():
    if not deps.message_router:
        return {"destinations": []}
    return {"destinations": deps.message_router.list_destinations()}


@router.post("")
async def add_destination(dest: DestinationCreate):
    if not deps.message_router:
        return {"error": "Router not initialized"}
    config = DestinationConfig(**dest.model_dump())
    deps.message_router.add_destination(config)
    return {"status": "added", "name": dest.name}


@router.put("/{name}")
async def update_destination(name: str, update: DestinationUpdate):
    if not deps.message_router:
        return {"error": "Router not initialized"}
    kwargs = {k: v for k, v in update.model_dump().items() if v is not None}
    success = deps.message_router.update_destination(name, **kwargs)
    return {"status": "updated" if success else "not_found"}


@router.delete("/{name}")
async def remove_destination(name: str):
    if not deps.message_router:
        return {"error": "Router not initialized"}
    success = deps.message_router.remove_destination(name)
    return {"status": "removed" if success else "not_found"}
