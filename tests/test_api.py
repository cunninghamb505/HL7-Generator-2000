"""Tests for the FastAPI routes."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.app import bootstrap
from src.core.config import SimulatorConfig
from src.web.api import create_app


@pytest.fixture
def app():
    config = SimulatorConfig()
    config.patient_pool.pool_size = 10
    bootstrap(config)
    return create_app()


@pytest.mark.asyncio
async def test_metrics_endpoint(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/metrics")
        assert resp.status_code == 200
        data = resp.json()
        assert "status" in data
        assert "messages_sent" in data


@pytest.mark.asyncio
async def test_patients_endpoint(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/patients")
        assert resp.status_code == 200
        data = resp.json()
        assert "patients" in data
        assert data["total"] == 10


@pytest.mark.asyncio
async def test_messages_endpoint(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/messages")
        assert resp.status_code == 200
        data = resp.json()
        assert "messages" in data


@pytest.mark.asyncio
async def test_workflows_endpoint(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/workflows")
        assert resp.status_code == 200
        data = resp.json()
        assert "workflows" in data


@pytest.mark.asyncio
async def test_destinations_endpoint(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/destinations")
        assert resp.status_code == 200
        data = resp.json()
        assert "destinations" in data


@pytest.mark.asyncio
async def test_control_endpoints(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/api/control/start")
        assert resp.status_code == 200

        resp = await client.post("/api/control/pause")
        assert resp.status_code == 200

        resp = await client.post("/api/control/stop")
        assert resp.status_code == 200


@pytest.mark.asyncio
async def test_login_page(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/login")
        assert resp.status_code == 200
        assert "Sign in" in resp.text


@pytest.mark.asyncio
async def test_dashboard_redirects_to_login(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=False) as client:
        resp = await client.get("/")
        assert resp.status_code == 303
        assert "/login" in resp.headers["location"]


@pytest.mark.asyncio
async def test_login_flow(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test", follow_redirects=False) as client:
        # Login with correct credentials
        resp = await client.post("/login", data={"username": "admin", "password": "admin"})
        assert resp.status_code == 303
        assert "/" == resp.headers["location"]

        # Extract session cookie and access dashboard
        cookies = resp.cookies
        resp = await client.get("/", cookies=cookies)
        assert resp.status_code == 200
        assert "HL7" in resp.text


@pytest.mark.asyncio
async def test_login_wrong_password(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.post("/login", data={"username": "admin", "password": "wrong"})
        assert resp.status_code == 401
        assert "Invalid" in resp.text
