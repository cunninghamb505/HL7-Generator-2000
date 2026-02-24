"""Message log API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

from src.validators.message_validator import validate_message
from src.web.dependencies import deps

router = APIRouter(prefix="/api/messages", tags=["messages"])


@router.get("")
async def list_messages(
    query: str = "",
    message_type: str = "",
    limit: int = Query(default=50, le=500),
    offset: int = Query(default=0, ge=0),
):
    if not deps.message_log:
        return {"messages": [], "total": 0}

    if query or message_type:
        messages = deps.message_log.search(
            query=query, message_type=message_type,
            limit=limit, offset=offset,
        )
    else:
        messages = deps.message_log.get_recent(limit)

    return {
        "messages": messages,
        "total": deps.message_log.total_count,
    }


@router.get("/{index}/validate")
async def validate_message_by_index(index: int):
    """On-demand validation of a logged message by its buffer index."""
    if not deps.message_log:
        return {"error": "Message log not initialized"}

    entry = deps.message_log.get_by_index(index)
    if not entry:
        return {"error": "Message not found"}

    result = validate_message(entry.raw_message, entry.message_type)
    return result.to_dict()


@router.delete("")
async def clear_messages():
    if deps.message_log:
        deps.message_log.clear()
    return {"status": "cleared"}
