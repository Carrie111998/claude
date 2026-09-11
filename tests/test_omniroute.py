"""Tests for OmniRoute API endpoints."""

import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.dependencies import get_omniroute_client
from app.omniroute.client import OmniRouteClient


AGENT_FIXTURE = {
    "id": "agent-001",
    "name": "Test Agent",
    "description": "A test agent",
    "endpoint_url": "https://agents.example.com/test",
    "capabilities": [],
    "metadata": {},
    "status": "active",
}


@pytest.fixture
def mock_client() -> OmniRouteClient:
    client = AsyncMock(spec=OmniRouteClient)
    client.list_agents.return_value = [AGENT_FIXTURE]
    client.get_agent.return_value = AGENT_FIXTURE
    client.create_agent.return_value = AGENT_FIXTURE
    client.delete_agent.return_value = None
    return client


@pytest.fixture
def override_dependency(mock_client):
    app.dependency_overrides[get_omniroute_client] = lambda: mock_client
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(override_dependency):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.mark.anyio
async def test_list_agents(async_client, mock_client):
    response = await async_client.get("/api/v1/omniroute/agents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "agent-001"


@pytest.mark.anyio
async def test_get_agent(async_client, mock_client):
    response = await async_client.get("/api/v1/omniroute/agents/agent-001")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Agent"
    mock_client.get_agent.assert_called_once_with("agent-001")


@pytest.mark.anyio
async def test_add_agent_from_omniroute(async_client, mock_client):
    payload = {"agent_id": "agent-001", "alias": "my-agent"}
    response = await async_client.post("/api/v1/omniroute/agents/add", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "agent-001"
    assert data["alias"] == "my-agent"


@pytest.mark.anyio
async def test_add_agent_without_alias(async_client, mock_client):
    payload = {"agent_id": "agent-001"}
    response = await async_client.post("/api/v1/omniroute/agents/add", json=payload)
    assert response.status_code == 200
    assert response.json()["id"] == "agent-001"


@pytest.mark.anyio
async def test_create_agent(async_client, mock_client):
    payload = {
        "name": "New Agent",
        "endpoint_url": "https://agents.example.com/new",
    }
    response = await async_client.post("/api/v1/omniroute/agents", json=payload)
    assert response.status_code == 201


@pytest.mark.anyio
async def test_delete_agent(async_client, mock_client):
    response = await async_client.delete("/api/v1/omniroute/agents/agent-001")
    assert response.status_code == 204
    mock_client.delete_agent.assert_called_once_with("agent-001")


@pytest.mark.anyio
async def test_health(async_client):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
