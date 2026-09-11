# Local Setup Guide - OmniRoute Agent Service

Complete step-by-step instructions to set up and run the project locally.

## Prerequisites

- Python 3.11+ ([Download](https://www.python.org/downloads/))
- Git ([Download](https://git-scm.com/downloads))
- Your OmniRoute API key: `sk-9f376f4c3ea8ffe3-39450a-242cd750`

## Step 1: Clone the Repository

```bash
git clone https://github.com/Carrie111998/claude.git
cd claude
```

## Step 2: Create Python Virtual Environment (Recommended)

### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

## Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**What gets installed:**
- fastapi (web framework)
- uvicorn (ASGI server)
- sqlalchemy (database ORM)
- httpx (async HTTP client)
- pydantic (data validation)
- pytest (testing)
- mcp (Model Context Protocol)

## Step 4: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OmniRoute API key
```

Open `.env` in your editor and set:
```env
OMNIROUTE_API_KEY=sk-9f376f4c3ea8ffe3-39450a-242cd750
OMNIROUTE_ENDPOINT=public
DEBUG=false
```

### Choose Your Endpoint

Select which OmniRoute endpoint to use via `OMNIROUTE_ENDPOINT`:

- **public** (default): `https://omniroute-0lvo.srv1854512.hstgr.cloud/v1`
- **cloudflare**: `https://occasions-idol-increasingly-tested.trycloudflare.com/v1`
- **local**: `http://localhost:20128/v1`
- **network**: `http://172.16.1.2:20128/v1`

Each endpoint can be used depending on your deployment setup. Change `OMNIROUTE_ENDPOINT` and restart the server to switch endpoints.

## Step 5: Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_omniroute.py -v

# Run with coverage
pytest tests/ --cov=app
```

Expected output: **15/15 tests passing** ✅

## Step 6: Start the Server

```bash
uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

## Step 7: Test the API

Open a new terminal and test endpoints:

### Health Check
```bash
curl http://localhost:8000/health
# Response: {"status":"ok"}
```

### List Local Agents
```bash
curl http://localhost:8000/api/v1/agents
# Response: [] (empty array initially)
```

### **Test Models Endpoint** (Real Data!)
```bash
curl http://localhost:8000/api/v1/omniroute/models | jq .
```

This will return actual models from OmniRoute!

### Import an Agent
```bash
curl -X POST http://localhost:8000/api/v1/omniroute/agents/add \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "your-omniroute-agent-id",
    "alias": "my-agent"
  }'
```

### Save Locally
```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "local-agent-1",
    "name": "My Local Agent",
    "endpoint_url": "https://example.com/agent",
    "alias": "quick-access"
  }'
```

## Step 8: Interactive API Documentation

Visit in your browser:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

You can test all endpoints interactively here!

## Step 9: Use MCP Server (Claude Integration)

In a new terminal:
```bash
python app/mcp_server_main.py
```

This starts the MCP server that Claude can use.

## Project Structure

```
claude/
├── app/
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Configuration
│   ├── db.py                    # Database setup
│   ├── models.py                # SQLAlchemy models
│   ├── services.py              # Business logic
│   ├── dependencies.py          # Dependency injection
│   ├── mcp_server.py            # MCP server
│   ├── mcp_server_main.py       # MCP entry point
│   ├── local_agents_router.py   # Local agent endpoints
│   ├── schemas_local.py         # Local agent schemas
│   └── omniroute/
│       ├── client.py            # OmniRoute API client
│       ├── router.py            # OmniRoute endpoints
│       └── schemas.py           # OmniRoute schemas
├── tests/
│   ├── test_omniroute.py        # OmniRoute tests (7)
│   └── test_local_agents.py     # Persistence tests (8)
├── .env.example                 # Environment template
├── .env                         # Your config (DO NOT COMMIT)
├── agents.db                    # SQLite database (auto-created)
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── SETUP_LOCAL.md              # This file
```

## Database

- **Type**: SQLite
- **File**: `agents.db` (auto-created on first run)
- **Tables**: `agents` (stores local agents)
- **Location**: Project root directory

## Troubleshooting

### Port 8000 Already in Use
```bash
# Use a different port
uvicorn app.main:app --port 8001 --reload
```

### Module Not Found Errors
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Tests Failing
```bash
# Clear pytest cache
pytest --cache-clear

# Run with verbose output
pytest tests/ -vv -s
```

### Database Errors
```bash
# Delete the old database
rm agents.db

# It will auto-recreate on next run
python -c "from app.db import init_db; init_db()"
```

## Common Commands

```bash
# Start server
uvicorn app.main:app --reload

# Run tests
pytest tests/ -v

# Start MCP server
python app/mcp_server_main.py

# Check API health
curl http://localhost:8000/health

# View database
# Open agents.db with any SQLite viewer

# Stop server
# Press Ctrl+C in the terminal
```

## Next Steps

1. ✅ Clone and setup locally
2. ✅ Run tests to verify everything works
3. ✅ Start the server
4. ✅ Test the `/api/v1/omniroute/models` endpoint
5. ✅ Import agents from OmniRoute
6. ✅ Save agents locally
7. ✅ Use the MCP server with Claude

## Getting Help

Check these files for more info:
- `README.md` - Project overview
- `app/main.py` - App entry point
- `.env.example` - Environment variables
- `tests/` - Test examples

## API Documentation

Once running, interactive docs are at:
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
