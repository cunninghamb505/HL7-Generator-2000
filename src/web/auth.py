"""Session-based authentication for the web dashboard."""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import Request, Response
from fastapi.responses import RedirectResponse

# In-memory session store: token -> expiry
_sessions: dict[str, datetime] = {}

SESSION_COOKIE = "hl7gen_session"
SESSION_TTL_HOURS = 24


def _hash(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def create_session(response: Response) -> str:
    token = secrets.token_urlsafe(32)
    _sessions[_hash(token)] = datetime.now(timezone.utc) + timedelta(hours=SESSION_TTL_HOURS)
    response.set_cookie(
        SESSION_COOKIE,
        token,
        httponly=True,
        samesite="lax",
        max_age=SESSION_TTL_HOURS * 3600,
    )
    return token


def verify_session(request: Request) -> bool:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return False
    hashed = _hash(token)
    expiry = _sessions.get(hashed)
    if expiry is None or datetime.now(timezone.utc) > expiry:
        _sessions.pop(hashed, None)
        return False
    return True


def destroy_session(request: Request, response: Response) -> None:
    token = request.cookies.get(SESSION_COOKIE)
    if token:
        _sessions.pop(_hash(token), None)
    response.delete_cookie(SESSION_COOKIE)


def require_auth(request: Request) -> Response | None:
    """Return a redirect response if not authenticated, else None."""
    if verify_session(request):
        return None
    return RedirectResponse("/login", status_code=303)
