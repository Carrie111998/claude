"""Tests for local agent persistence."""

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, get_db
from app.schemas_local import LocalAgentCreate

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def override_get_db(db):
    """Override get_db dependency."""

    def _get_db():
        return db

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(override_get_db):
    """Create async test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


AGENT_DATA = {
    "id": "agent-001",
    "name": "Test Agent",
    "description": "A test agent",
    "endpoint_url": "https://example.com/agent",
    "alias": "test-alias",
}


@pytest.mark.anyio
async def test_create_local_agent(async_client):
    response = await async_client.post("/api/v1/agents", json=AGENT_DATA)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "agent-001"
    assert data["name"] == "Test Agent"
    assert data["alias"] == "test-alias"


@pytest.mark.anyio
async def test_create_duplicate_agent(async_client):
    # Create first agent
    await async_client.post("/api/v1/agents", json=AGENT_DATA)

    # Try to create duplicate
    response = await async_client.post("/api/v1/agents", json=AGENT_DATA)
    assert response.status_code == 409


@pytest.mark.anyio
async def test_get_local_agent(async_client):
    # Create agent
    await async_client.post("/api/v1/agents", json=AGENT_DATA)

    # Get agent
    response = await async_client.get("/api/v1/agents/agent-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "agent-001"
    assert data["name"] == "Test Agent"


@pytest.mark.anyio
async def test_get_nonexistent_agent(async_client):
    response = await async_client.get("/api/v1/agents/nonexistent")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_list_local_agents(async_client):
    # Create multiple agents
    for i in range(3):
        data = AGENT_DATA.copy()
        data["id"] = f"agent-{i:03d}"
        await async_client.post("/api/v1/agents", json=data)

    response = await async_client.get("/api/v1/agents")
    assert response.status_code == 200
    agents = response.json()
    assert len(agents) == 3


@pytest.mark.anyio
async def test_search_agents(async_client):
    # Create agents
    agents = [
        {**AGENT_DATA, "id": "agent-001", "name": "Python Agent"},
        {**AGENT_DATA, "id": "agent-002", "name": "JavaScript Agent"},
        {**AGENT_DATA, "id": "agent-003", "name": "Go Agent"},
    ]
    for agent in agents:
        await async_client.post("/api/v1/agents", json=agent)

    response = await async_client.get("/api/v1/agents/search?q=Python")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["name"] == "Python Agent"


@pytest.mark.anyio
async def test_update_agent(async_client):
    # Create agent
    await async_client.post("/api/v1/agents", json=AGENT_DATA)

    # Update agent
    update = {"name": "Updated Agent", "alias": "new-alias"}
    response = await async_client.put("/api/v1/agents/agent-001", json=update)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Agent"
    assert data["alias"] == "new-alias"


@pytest.mark.anyio
async def test_delete_agent(async_client):
    # Create agent
    await async_client.post("/api/v1/agents", json=AGENT_DATA)

    # Delete agent
    response = await async_client.delete("/api/v1/agents/agent-001")
    assert response.status_code == 204

    # Verify deleted
    response = await async_client.get("/api/v1/agents/agent-001")
    assert response.status_code == 404
