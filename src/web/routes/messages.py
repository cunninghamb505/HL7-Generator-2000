"""Message log API routes."""

from __future__ import annotations

from fastapi import APIRouter, Query

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


@router.delete("")
async def clear_messages():
    if deps.message_log:
        deps.message_log.clear()
    return {"status": "cleared"}
