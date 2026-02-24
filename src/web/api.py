"""FastAPI application factory."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

from src.web.dependencies import deps
from src.web.routes import control, dashboard, destinations, messages, metrics, workflows, patients


def create_app() -> FastAPI:
    app = FastAPI(
        title="HL7 Generator 2000",
        description="Hospital HL7v2 message simulator with web dashboard",
        version="1.0.0",
    )

    # Mount static files
    static_dir = Path(__file__).resolve().parent.parent.parent / "static"
    if static_dir.exists():
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    # Register API routes
    app.include_router(control.router)
    app.include_router(patients.router)
    app.include_router(messages.router)
    app.include_router(workflows.router)
    app.include_router(destinations.router)
    app.include_router(metrics.router)

    # Register HTML dashboard routes
    app.include_router(dashboard.router)

    # WebSocket endpoint
    @app.websocket("/ws")
    async def websocket_endpoint(ws: WebSocket):
        if not deps.ws_manager:
            await ws.close()
            return

        await deps.ws_manager.connect(ws)
        try:
            while True:
                # Keep connection alive; client doesn't send data
                await ws.receive_text()
        except WebSocketDisconnect:
            deps.ws_manager.disconnect(ws)

    return app
