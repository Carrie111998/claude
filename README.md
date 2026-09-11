# Claude Agent Service - OmniRoute Integration

A FastAPI service that provides REST endpoints to interact with the OmniRoute agent platform.

## Features

- **OmniRoute API Client**: Async HTTP client with support for agent CRUD operations
- **FastAPI Router**: RESTful endpoints for managing agents
- **Import Agents**: Add existing OmniRoute agents to the local system with optional aliases
- **Configuration**: Environment-based setup via `.env`
- **Tests**: Full test coverage with pytest and AsyncClient

## Quick Start

### 1. Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your OmniRoute credentials
# OMNIROUTE_API_KEY=sk-your-key-here
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
# Using uvicorn directly
uvicorn app.main:app --reload

# Server runs at http://localhost:8000
```

### 4. Test the API

```bash
# List all agents
curl http://localhost:8000/api/v1/omniroute/agents

# Import an agent from OmniRoute
curl -X POST http://localhost:8000/api/v1/omniroute/agents/add \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "agent-123",
    "alias": "my-local-agent"
  }'

# Create a new agent in OmniRoute
curl -X POST http://localhost:8000/api/v1/omniroute/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Agent",
    "description": "A custom agent",
    "endpoint_url": "https://myagent.example.com",
    "capabilities": []
  }'

# Health check
curl http://localhost:8000/health
```

## API Endpoints

### Agents

- `GET /api/v1/omniroute/agents` — List all agents
- `GET /api/v1/omniroute/agents/{id}` — Get a single agent
- **`POST /api/v1/omniroute/agents/add`** — Import agent from OmniRoute
- `POST /api/v1/omniroute/agents` — Create a new agent
- `DELETE /api/v1/omniroute/agents/{id}` — Delete an agent

### Utility

- `GET /health` — Health check

## Project Structure

```
app/
├── main.py              # FastAPI app setup
├── config.py            # Environment configuration
├── dependencies.py      # Dependency injection
└── omniroute/
    ├── client.py        # OmniRoute API client
    ├── router.py        # FastAPI router
    └── schemas.py       # Pydantic models

tests/
└── test_omniroute.py    # Endpoint tests
```

## Running Tests

```bash
# All tests
OMNIROUTE_API_KEY=test pytest tests/ -v

# Specific test
OMNIROUTE_API_KEY=test pytest tests/test_omniroute.py::test_list_agents -v
```

## Configuration

Environment variables (set in `.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `OMNIROUTE_BASE_URL` | `https://omniroute-0lvo.srv1854512.hstgr.cloud/v1` | OmniRoute API endpoint |
| `OMNIROUTE_API_KEY` | (required) | OmniRoute API key |
| `DEBUG` | `false` | Enable FastAPI debug mode |
| `APP_TITLE` | `Claude Agent Service` | App name in docs |
| `APP_VERSION` | `0.1.0` | App version |
