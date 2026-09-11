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
# List available models in OmniRoute
curl http://localhost:8000/api/v1/omniroute/models | jq .

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

### 5. Switch Endpoints

Edit `.env` to switch between endpoints:

```bash
# Use local OmniRoute instance
OMNIROUTE_ENDPOINT=local

# Or use Cloudflare tunnel
OMNIROUTE_ENDPOINT=cloudflare

# Then restart the server for the change to take effect
```

## API Endpoints

### OmniRoute Operations

- `GET /api/v1/omniroute/agents` — List all agents in OmniRoute
- `GET /api/v1/omniroute/agents/{id}` — Get a single OmniRoute agent
- **`POST /api/v1/omniroute/agents/add`** — **Import agent from OmniRoute**
- `POST /api/v1/omniroute/agents` — Register a new agent in OmniRoute
- `DELETE /api/v1/omniroute/agents/{id}` — Delete an agent from OmniRoute
- `GET /api/v1/omniroute/models` — List all available models in OmniRoute

### Local Agent Storage (Persistence)

- **`POST /api/v1/agents`** — **Save an agent locally**
- `GET /api/v1/agents` — List all locally saved agents
- `GET /api/v1/agents/{id}` — Get a specific local agent
- `GET /api/v1/agents/search?q=name` — Search agents by name/alias
- `PUT /api/v1/agents/{id}` — Update a local agent
- `DELETE /api/v1/agents/{id}` — Delete a local agent

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

## Local Agent Persistence

Agents imported from OmniRoute can be saved locally with SQLite for offline access and caching.

```bash
# Save an imported agent locally
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "my-agent-123",
    "name": "My Saved Agent",
    "endpoint_url": "https://agents.example.com/my-agent",
    "alias": "quick-agent",
    "omniroute_id": "omniroute-id-here"
  }'

# Search local agents
curl 'http://localhost:8000/api/v1/agents/search?q=python'

# Get all saved agents
curl http://localhost:8000/api/v1/agents

# Update an agent
curl -X PUT http://localhost:8000/api/v1/agents/my-agent-123 \
  -H "Content-Type: application/json" \
  -d '{"alias": "new-alias"}'
```

**Database:** SQLite (`agents.db` in project root)

## MCP Server Integration

The service includes an MCP (Model Context Protocol) server that exposes both OmniRoute and local agent operations as tools for Claude and other AI assistants.

### Run MCP Server Standalone

```bash
# Start the MCP server
OMNIROUTE_API_KEY=sk-your-key-here python app/mcp_server_main.py
```

### Use with Claude Code

1. Add your API key to `.env`:
   ```
   OMNIROUTE_API_KEY=sk-your-key-here
   ```

2. The MCP server is configured in `.claude/settings.json` and will be available to Claude Code automatically.

### Available MCP Tools

- `omniroute_list_agents` — List all agents
- `omniroute_get_agent` — Get a single agent by ID
- `omniroute_add_agent` — Import an agent with optional alias
- `omniroute_create_agent` — Register a new agent
- `omniroute_delete_agent` — Delete an agent

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
| `OMNIROUTE_API_KEY` | (required) | OmniRoute API key |
| `OMNIROUTE_ENDPOINT` | `public` | Endpoint to use: `public`, `cloudflare`, `local`, or `network` |
| `DEBUG` | `false` | Enable FastAPI debug mode |
| `APP_TITLE` | `Claude Agent Service` | App name in docs |
| `APP_VERSION` | `0.1.0` | App version |

### Multiple Endpoint Support

The service supports multiple OmniRoute endpoints for different deployment scenarios:

```bash
# Public endpoint (default)
OMNIROUTE_ENDPOINT=public
# https://omniroute-0lvo.srv1854512.hstgr.cloud/v1

# Cloudflare tunnel endpoint
OMNIROUTE_ENDPOINT=cloudflare
# https://occasions-idol-increasingly-tested.trycloudflare.com/v1

# Local network endpoint
OMNIROUTE_ENDPOINT=local
# http://localhost:20128/v1

# Internal network endpoint
OMNIROUTE_ENDPOINT=network
# http://172.16.1.2:20128/v1
```

Each endpoint can be selected via the `OMNIROUTE_ENDPOINT` environment variable. This allows seamless switching between cloud, Cloudflare tunnel, and local deployments.
