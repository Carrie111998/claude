# Testing the Models Endpoint

Complete guide to test the `/api/v1/omniroute/models` endpoint locally with your real OmniRoute API key.

## Prerequisites

- Local setup complete (see `SETUP_LOCAL.md`)
- OmniRoute API key: `sk-9f376f4c3ea8ffe3-39450a-242cd750`
- Server running on `http://127.0.0.1:8000`

## Method 1: cURL (Command Line)

### Start the server
```bash
export OMNIROUTE_API_KEY="sk-9f376f4c3ea8ffe3-39450a-242cd750"
uvicorn app.main:app --reload
```

### Test in another terminal
```bash
# Simple test
curl http://localhost:8000/api/v1/omniroute/models

# Pretty print JSON response
curl http://localhost:8000/api/v1/omniroute/models | jq .

# With verbose output
curl -v http://localhost:8000/api/v1/omniroute/models

# Save response to file
curl http://localhost:8000/api/v1/omniroute/models > models.json
```

## Method 2: Interactive API Documentation (Recommended)

1. **Start the server**
   ```bash
   export OMNIROUTE_API_KEY="sk-9f376f4c3ea8ffe3-39450a-242cd750"
   uvicorn app.main:app --reload
   ```

2. **Open browser**
   - Go to: `http://127.0.0.1:8000/docs`

3. **Find `/api/v1/omniroute/models`**
   - Scroll down to "omniroute" section
   - Find the green GET endpoint

4. **Click "Try it out"**
   - Click the button
   - Click "Execute"
   - View the response!

## Method 3: Python Script

Create a file `test_models.py`:

```python
import asyncio
import httpx
import json
from app.omniroute.client import OmniRouteClient

async def test_models():
    client = OmniRouteClient(
        base_url="https://omniroute-0lvo.srv1854512.hstgr.cloud/v1",
        api_key="sk-9f376f4c3ea8ffe3-39450a-242cd750"
    )
    
    try:
        print("Fetching OmniRoute models...")
        models = await client.list_models()
        print("\n✅ Models retrieved successfully!\n")
        print(json.dumps(models, indent=2))
        return models
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        return None

if __name__ == "__main__":
    asyncio.run(test_models())
```

Run it:
```bash
cd /path/to/claude
export OMNIROUTE_API_KEY="sk-9f376f4c3ea8ffe3-39450a-242cd750"
python test_models.py
```

## Method 4: Python Requests in Python Shell

```python
import subprocess
import json

# Make request
result = subprocess.run(
    ["curl", "http://localhost:8000/api/v1/omniroute/models"],
    capture_output=True,
    text=True
)

# Parse response
models = json.loads(result.stdout)
print(json.dumps(models, indent=2))
```

## Expected Response

The endpoint returns a JSON array of available models. Example structure:

```json
[
  {
    "id": "claude-3-5-sonnet",
    "name": "Claude 3.5 Sonnet",
    "type": "llm",
    "provider": "anthropic",
    "capabilities": ["text", "vision"],
    "context_window": 200000,
    "pricing": {
      "input": "0.003",
      "output": "0.015"
    }
  },
  {
    "id": "gpt-4-turbo",
    "name": "GPT-4 Turbo",
    "type": "llm",
    "provider": "openai",
    "capabilities": ["text", "vision"],
    "context_window": 128000
  },
  {
    "id": "llama-2-70b",
    "name": "Llama 2 70B",
    "type": "llm",
    "provider": "meta",
    "capabilities": ["text"],
    "context_window": 4096
  }
]
```

## Troubleshooting

### Server Not Running
```
Connection refused
```
**Solution**: Start the server first
```bash
export OMNIROUTE_API_KEY="sk-9f376f4c3ea8ffe3-39450a-242cd750"
uvicorn app.main:app --reload
```

### 500 Internal Server Error
```
Internal Server Error
```
**Check logs**: Look at server output for detailed error
- Network issues connecting to OmniRoute
- Invalid API key
- OmniRoute service down

**Solution**: 
- Verify API key in `.env`
- Check OmniRoute service status
- Look at server logs: `tail -f /tmp/server.log` (on Linux/Mac)

### 401 Unauthorized
```
{"detail": "Unauthorized"}
```
**Solution**: Check your API key
- Verify `OMNIROUTE_API_KEY` env var is set
- Verify key is correct: `sk-9f376f4c3ea8ffe3-39450a-242cd750`

### 404 Not Found
```
{"detail": "Not Found"}
```
**Solution**: URL is wrong
- Correct: `http://localhost:8000/api/v1/omniroute/models`
- Check spelling and path

## Testing Other Endpoints

### List Local Agents
```bash
curl http://localhost:8000/api/v1/agents | jq .
```

### Save a Local Agent
```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "test-agent",
    "name": "Test Agent",
    "endpoint_url": "https://example.com/agent"
  }' | jq .
```

### List OmniRoute Agents
```bash
curl http://localhost:8000/api/v1/omniroute/agents | jq .
```

### Import Agent from OmniRoute
```bash
curl -X POST http://localhost:8000/api/v1/omniroute/agents/add \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "some-omniroute-agent-id",
    "alias": "my-agent"
  }' | jq .
```

## Automated Test Suite

Run all tests:
```bash
pytest tests/ -v
```

Run only models-related tests:
```bash
pytest tests/test_omniroute.py -v -k "agent"
```

## Next Steps

Once models endpoint works:

1. ✅ **Explore Models** - See what models are available
2. ✅ **List Agents** - Check available agents in OmniRoute
3. ✅ **Import Agent** - Use `/omniroute/agents/add` endpoint
4. ✅ **Save Locally** - Use `/agents` endpoint to save locally
5. ✅ **Search** - Use `/agents/search` to find agents

## Performance Notes

- First request may take 2-3 seconds (connection establishment)
- Subsequent requests are faster (connection reuse)
- Response cached locally in `agents.db` if saved

## API Documentation

For interactive testing with automatic schema validation:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`
- **OpenAPI JSON**: `http://127.0.0.1:8000/openapi.json`
