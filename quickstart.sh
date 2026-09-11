#!/bin/bash
# Quick Start Script for OmniRoute Agent Service

set -e

echo "🚀 OmniRoute Agent Service - Quick Start"
echo "=========================================="
echo ""

# Check Python
echo "✓ Checking Python..."
python3 --version || { echo "❌ Python 3 not found. Install from https://www.python.org/downloads/"; exit 1; }

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "✓ Installing dependencies..."
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

# Setup .env file
if [ ! -f ".env" ]; then
    echo "✓ Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env and add your OmniRoute API key:"
    echo "   OMNIROUTE_API_KEY=sk-9f376f4c3ea8ffe3-39450a-242cd750"
    echo ""
fi

# Run tests
echo ""
echo "✓ Running tests..."
python -m pytest tests/ -q

# Start server
echo ""
echo "✅ Setup complete!"
echo ""
echo "Starting server on http://127.0.0.1:8000"
echo ""
echo "Available endpoints:"
echo "  • GET  http://127.0.0.1:8000/health"
echo "  • GET  http://127.0.0.1:8000/docs (Interactive API docs)"
echo "  • GET  http://127.0.0.1:8000/api/v1/omniroute/models"
echo "  • GET  http://127.0.0.1:8000/api/v1/agents"
echo ""
echo "Press Ctrl+C to stop"
echo ""

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
