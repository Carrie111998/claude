# VPS Deployment Guide - OmniRoute API Agent Service

Complete guide to deploy the OmniRoute Agent Service on your VPS alongside your existing OmniRoute instance.

## Prerequisites

- VPS with Linux (Ubuntu/Debian recommended)
- Python 3.11+
- Git installed
- Port 8001 or 8002 available for the API service
- SSH access to VPS

## Quick Deployment (5 minutes)

### Step 1: SSH into Your VPS

```bash
ssh user@your-vps-ip
cd /opt  # or your preferred directory
```

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Carrie111998/claude.git
cd claude

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
nano .env
```

Edit `.env` and set:
```env
OMNIROUTE_API_KEY=sk-9f376f4c3ea8ffe3-39450a-242cd750
OMNIROUTE_ENDPOINT=local
DEBUG=false
```

### Step 4: Test

```bash
# Run tests
python -m pytest tests/ -v

# Start server (temporary test)
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

Visit in browser or curl:
```bash
curl http://your-vps-ip:8001/health
curl http://your-vps-ip:8001/api/v1/omniroute/models
```

## Production Deployment (Recommended)

### Option 1: Systemd Service (Recommended)

Create `/etc/systemd/system/omniroute-agent.service`:

```ini
[Unit]
Description=OmniRoute Agent Service
After=network.target

[Service]
Type=notify
User=nobody
WorkingDirectory=/opt/claude
Environment="PATH=/opt/claude/venv/bin"
Environment="OMNIROUTE_API_KEY=sk-9f376f4c3ea8ffe3-39450a-242cd750"
Environment="OMNIROUTE_ENDPOINT=local"
Environment="DEBUG=false"
ExecStart=/opt/claude/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable omniroute-agent
sudo systemctl start omniroute-agent
sudo systemctl status omniroute-agent
```

View logs:
```bash
sudo journalctl -u omniroute-agent -f
```

### Option 2: Docker (If Docker Available)

```bash
# Build Docker image
docker build -t omniroute-agent .

# Run container
docker run -d \
  --name omniroute-agent \
  -e OMNIROUTE_API_KEY=sk-9f376f4c3ea8ffe3-39450a-242cd750 \
  -e OMNIROUTE_ENDPOINT=local \
  -p 8001:8000 \
  omniroute-agent
```

### Option 3: Process Manager (Gunicorn)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8001 --env OMNIROUTE_ENDPOINT=local app.main:app
```

## Choosing Your Endpoint

Switch between endpoints in your `.env`:

```bash
# Local (Fastest - recommended for production)
OMNIROUTE_ENDPOINT=local
# http://localhost:20128/v1

# Network (Internal IP)
OMNIROUTE_ENDPOINT=network
# http://172.16.1.2:20128/v1

# Cloudflare (Secure external tunnel)
OMNIROUTE_ENDPOINT=cloudflare
# https://occasions-idol-increasingly-tested.trycloudflare.com/v1

# Public (Cloud endpoint)
OMNIROUTE_ENDPOINT=public
# https://omniroute-0lvo.srv1854512.hstgr.cloud/v1
```

After changing endpoint, restart the service:
```bash
sudo systemctl restart omniroute-agent
```

## Testing Your Deployment

### Health Check
```bash
curl http://your-vps-ip:8001/health
# Response: {"status":"ok"}
```

### Test Models Endpoint
```bash
curl http://your-vps-ip:8001/api/v1/omniroute/models | jq .
```

### List Agents
```bash
curl http://your-vps-ip:8001/api/v1/omniroute/agents | jq .
```

### Save Agent Locally
```bash
curl -X POST http://your-vps-ip:8001/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "id": "agent-1",
    "name": "My Agent",
    "endpoint_url": "https://example.com/agent",
    "alias": "quick-agent"
  }'
```

## Endpoint Testing Utility

Test all configured endpoints:

```bash
python test_endpoints.py
```

Output will show:
```
✅ PUBLIC     | https://omniroute-0lvo.srv1854512.hstgr.cloud/v1
✅ CLOUDFLARE | https://occasions-idol-increasingly-tested.trycloudflare.com/v1
✅ LOCAL      | http://localhost:20128/v1
✅ NETWORK    | http://172.16.1.2:20128/v1
```

## Database Management

SQLite database is automatically created at `agents.db`:

```bash
# View database
sqlite3 agents.db ".tables"

# Backup database
cp agents.db agents.db.backup

# Clear agents (if needed)
rm agents.db
# Will recreate on next restart
```

## Firewall Configuration

Allow access on port 8001:

### UFW (Ubuntu)
```bash
sudo ufw allow 8001/tcp
```

### iptables
```bash
sudo iptables -A INPUT -p tcp --dport 8001 -j ACCEPT
```

### Behind Nginx/Apache
Proxy requests from port 80/443 to 8001:

```nginx
location /api/omniroute {
    proxy_pass http://127.0.0.1:8001;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

## Monitoring

### Check Service Status
```bash
sudo systemctl status omniroute-agent
```

### View Real-time Logs
```bash
sudo journalctl -u omniroute-agent -f
```

### Monitor Performance
```bash
# CPU and memory usage
top -p $(pgrep -f "uvicorn app.main:app")

# Check open ports
netstat -tlnp | grep 8001
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8001
lsof -i :8001

# Kill process
kill -9 <PID>

# Or use different port in service file
# Change --port 8001 to --port 8002
```

### Import Errors
```bash
# Reinstall dependencies
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Database Locked
```bash
# Check for stale processes
ps aux | grep python

# Remove lock file if exists
rm agents.db-wal agents.db-shm 2>/dev/null

# Restart service
sudo systemctl restart omniroute-agent
```

### Connection to OmniRoute Failing
```bash
# Test connectivity to OmniRoute
curl -H "Authorization: Bearer sk-9f376f4c3ea8ffe3-39450a-242cd750" \
  http://localhost:20128/v1/agents

# Check firewall
sudo ufw status
sudo iptables -L | grep 20128
```

## Updates & Maintenance

### Pull Latest Changes
```bash
cd /opt/claude
git pull origin main
# Restart service
sudo systemctl restart omniroute-agent
```

### Update Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
sudo systemctl restart omniroute-agent
```

### Database Backup Cron Job
```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * cp /opt/claude/agents.db /opt/claude/backups/agents.db.$(date +\%Y\%m\%d)
```

## API Documentation

Access interactive API docs at `http://your-vps-ip:8001/docs`

### Available Endpoints

**OmniRoute Operations:**
- `GET /api/v1/omniroute/agents` - List all agents in OmniRoute
- `GET /api/v1/omniroute/agents/{id}` - Get single agent
- `POST /api/v1/omniroute/agents/add` - Import agent
- `POST /api/v1/omniroute/agents` - Create new agent
- `DELETE /api/v1/omniroute/agents/{id}` - Delete agent
- `GET /api/v1/omniroute/models` - List available models

**Local Storage:**
- `GET /api/v1/agents` - List locally saved agents
- `GET /api/v1/agents/{id}` - Get local agent
- `POST /api/v1/agents` - Save agent locally
- `PUT /api/v1/agents/{id}` - Update agent
- `DELETE /api/v1/agents/{id}` - Delete agent
- `GET /api/v1/agents/search?q=term` - Search agents

**Utility:**
- `GET /health` - Health check
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

## Next Steps

1. ✅ Deploy service to VPS
2. ✅ Configure to use local endpoint
3. ✅ Test all endpoints
4. ✅ Set up systemd service for auto-start
5. ✅ Enable firewall access
6. ✅ Configure backups
7. 📍 Add reverse proxy if needed (Nginx/Apache)
8. 📍 Set up SSL/TLS for external access

## Support

For issues or questions, check:
- `README.md` - Project overview
- `SETUP_LOCAL.md` - Local development setup
- `TEST_MODELS_ENDPOINT.md` - Endpoint testing guide

---

**Ready to deploy! 🚀**
