"""Dashboard HTML page routes."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.web.auth import create_session, destroy_session, require_auth, verify_session
from src.web.dependencies import deps

router = APIRouter(tags=["dashboard"])

# Resolve templates directory: src/web/routes -> src/web -> src -> src/templates
_src_dir = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(_src_dir / "templates"))


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    if verify_session(request):
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
async def login_submit(request: Request):
    form = await request.form()
    username = form.get("username", "")
    password = form.get("password", "")

    if deps.auth_config and username == deps.auth_config.username and password == deps.auth_config.password:
        response = RedirectResponse("/", status_code=303)
        create_session(response)
        return response

    return templates.TemplateResponse(request, "login.html", {
        "error": "Invalid username or password",
    }, status_code=401)


@router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse("/login", status_code=303)
    destroy_session(request, response)
    return response


@router.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "dashboard.html", {
        "page": "dashboard",
    })


@router.get("/messages", response_class=HTMLResponse)
async def messages_page(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "messages.html", {
        "page": "messages",
    })


@router.get("/patients", response_class=HTMLResponse)
async def patients_page(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "patients.html", {
        "page": "patients",
    })


@router.get("/workflows", response_class=HTMLResponse)
async def workflows_page(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "workflows.html", {
        "page": "workflows",
    })


@router.get("/destinations", response_class=HTMLResponse)
async def destinations_page(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "destinations.html", {
        "page": "destinations",
    })


@router.get("/patients/{mrn}/timeline", response_class=HTMLResponse)
async def timeline_page(request: Request, mrn: str):
    redirect = require_auth(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "timeline.html", {
        "page": "patients",
        "mrn": mrn,
    })


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    redirect = require_auth(request)
    if redirect:
        return redirect
    return templates.TemplateResponse(request, "settings.html", {
        "page": "settings",
    })
