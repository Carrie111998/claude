# OmniRoute MCP Server Setup

Enable Claude to access OmniRoute models and agents through the Model Context Protocol (MCP).

## What is MCP?

MCP (Model Context Protocol) allows Claude to:
- Call tools you define
- Access resources (models, agents, etc.)
- Interact with external systems
- Execute complex workflows

## Setup Steps

### Step 1: Deploy MCP Server on VPS

Copy the systemd service file to your VPS:

```bash
# On your VPS
sudo nano /etc/systemd/system/omniroute-mcp.service
```

Paste this configuration:

```ini
[Unit]
Description=OmniRoute MCP Server
After=network.target omniroute-agent.service
Requires=omniroute-agent.service

[Service]
Type=simple
User=nobody
WorkingDirectory=/opt/claude
Environment="PATH=/opt/claude/venv/bin"
Environment="OMNIROUTE_API_KEY=sk-9f376f4c3ea8ffe3-39450a-242cd750"
Environment="OMNIROUTE_ENDPOINT=local"
Environment="DEBUG=false"
ExecStart=/opt/claude/venv/bin/python3 -m app.mcp_server
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable omniroute-mcp
sudo systemctl start omniroute-mcp
sudo systemctl status omniroute-mcp
```

### Step 2: Configure Claude to Connect

**Option A: Claude Code CLI (Local)**

If running Claude Code locally, add to your claude config (usually `~/.claude/settings.json` or `~/.config/claude/settings.json`):

```json
{
  "mcpServers": {
    "omniroute": {
      "command": "python3",
      "args": ["-m", "app.mcp_server"],
      "cwd": "/path/to/claude/project",
      "env": {
        "OMNIROUTE_API_KEY": "sk-9f376f4c3ea8ffe3-39450a-242cd750",
        "OMNIROUTE_ENDPOINT": "local"
      }
    }
  }
}
```

**Option B: Claude Web (claude.ai)**

For claude.ai web interface, configure via Claude Code remote environment at https://code.claude.com/docs/en/claude-code-on-the-web

### Step 3: Test MCP Integration

In Claude, ask:
```
List the OmniRoute models
```

Claude should automatically:
1. Discover the MCP server
2. Call the `omniroute_list_models` tool
3. Return the model list

## Available MCP Tools

### Local Agent Storage
- `local_list_agents` - List locally stored agents
- `local_get_agent` - Get a specific local agent

### OmniRoute Models & Agents
- `omniroute_list_models` - List available models
- `omniroute_list_agents` - List OmniRoute agents
- `omniroute_get_agent` - Fetch a specific agent
- `omniroute_add_agent` - Import an agent
- `omniroute_create_agent` - Create a new agent
- `omniroute_delete_agent` - Delete an agent

## Example Usage

### Ask Claude to list models:
```
"What models are available in OmniRoute?"
```

Claude will:
1. Call `omniroute_list_models` 
2. Parse the response
3. Present available models

### Ask Claude to manage agents:
```
"Show me all OmniRoute agents"
```

Claude will:
1. Call `omniroute_list_agents`
2. Display agent information
3. Allow you to import or create agents

### Complex workflows:
```
"Create a new agent called 'my-research-agent' with endpoint https://research.example.com 
and add it to OmniRoute"
```

Claude will:
1. Call `omniroute_create_agent` with your specifications
2. Confirm the agent was created
3. Save it locally if needed

## Troubleshooting

### MCP Server not starting
```bash
# Check logs
sudo journalctl -u omniroute-mcp -f

# Manual test
cd /opt/claude
OMNIROUTE_ENDPOINT=local python3 -m app.mcp_server
```

### Claude can't find MCP server
1. Verify service is running: `sudo systemctl status omniroute-mcp`
2. Check configuration file syntax (JSON must be valid)
3. Restart Claude Code after changing configuration
4. Verify environment variables are set correctly

### Tool calls failing
```bash
# Test the OmniRoute API directly
curl http://localhost:8001/api/v1/omniroute/models

# Test the MCP server manually
python3 -c "
import asyncio
from app.mcp_server import server
asyncio.run(server.list_tools())
"
```

### Models endpoint returns error
1. Verify Agent Service is running: `sudo systemctl status omniroute-agent`
2. Check OmniRoute is accessible: `curl http://localhost:32769/v1/agents -H "Authorization: Bearer sk-9f376f4c3ea8ffe3-39450a-242cd750"`
3. Check logs: `sudo journalctl -u omniroute-agent -f`

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Claude (local or web)                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │ MCP Protocol (stdio/SSE)
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ OmniRoute MCP Server (mcp_server.py)                       │
│ - list_tools()                                             │
│ - call_tool(name, arguments)                              │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP REST API
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Agent Service (main.py) - Port 8001                        │
│ - /api/v1/omniroute/models                                │
│ - /api/v1/omniroute/agents                                │
│ - /api/v1/agents (local storage)                          │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/AsyncIO
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ OmniRoute API (Port 32769)                                 │
│ - Models, Agents, Configurations                          │
└─────────────────────────────────────────────────────────────┘
```

## Production Considerations

1. **Security:**
   - Keep API key in environment variables
   - Use systemd for secure service management
   - Restrict network access to MCP server if exposed

2. **Performance:**
   - MCP server runs in same Python process
   - Async operations for non-blocking calls
   - Connection pooling via httpx client

3. **Monitoring:**
   - Check logs: `journalctl -u omniroute-mcp -f`
   - Monitor memory: Top or systemd resource controls
   - Health endpoint: `curl http://localhost:8001/health`

## Next Steps

1. ✅ Deploy MCP server systemd service
2. ✅ Configure Claude to connect
3. ✅ Test with "List OmniRoute models"
4. 📍 Create custom agents in Claude
5. 📍 Build complex workflows using Claude + OmniRoute

---

**Questions?** Check:
- `README.md` - Project overview
- `DEPLOY_VPS.md` - VPS deployment guide
- `SETUP_LOCAL.md` - Local development
