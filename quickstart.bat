@echo off
REM Quick Start Script for OmniRoute Agent Service (Windows)

setlocal enabledelayedexpansion

echo.
echo 🚀 OmniRoute Agent Service - Quick Start
echo ==========================================
echo.

REM Check Python
echo ✓ Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Install from https://www.python.org/downloads/
    exit /b 1
)

REM Create virtual environment
if not exist "venv" (
    echo ✓ Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✓ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo ✓ Installing dependencies...
python -m pip --quiet --upgrade pip
pip install --quiet -r requirements.txt

REM Setup .env file
if not exist ".env" (
    echo ✓ Creating .env file...
    copy .env.example .env
    echo.
    echo ⚠️  Please edit .env and add your OmniRoute API key:
    echo    OMNIROUTE_API_KEY=sk-9f376f4c3ea8ffe3-39450a-242cd750
    echo.
)

REM Run tests
echo.
echo ✓ Running tests...
python -m pytest tests/ -q

REM Start server
echo.
echo ✅ Setup complete!
echo.
echo Starting server on http://127.0.0.1:8000
echo.
echo Available endpoints:
echo   • GET  http://127.0.0.1:8000/health
echo   • GET  http://127.0.0.1:8000/docs (Interactive API docs)
echo   • GET  http://127.0.0.1:8000/api/v1/omniroute/models
echo   • GET  http://127.0.0.1:8000/api/v1/agents
echo.
echo Press Ctrl+C to stop
echo.

uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

endlocal
