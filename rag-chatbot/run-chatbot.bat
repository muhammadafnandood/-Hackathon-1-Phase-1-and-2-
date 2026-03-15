@echo off
echo ============================================================
echo   RAG Chatbot - Complete Setup and Run Script
echo ============================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org
    exit /b 1
)

echo [1/4] Checking Python installation...
echo ✓ Python is installed
echo.

REM Check if dependencies are installed
echo [2/4] Checking dependencies...
python -c "import fastapi" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    cd /d %~dp0
    python -m pip install fastapi uvicorn python-dotenv -q
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        exit /b 1
    )
    echo ✓ Dependencies installed
) else (
    echo ✓ Dependencies already installed
)
echo.

REM Check if vector store exists
echo [3/4] Checking vector store...
if not exist "backend\vector_store.db" (
    echo Creating vector store...
    cd backend
    python simple_ingest.py --docs-dir ../book/docs
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create vector store
        cd ..
        exit /b 1
    )
    cd ..
    echo ✓ Vector store created
) else (
    echo ✓ Vector store already exists
)
echo.

REM Start the server
echo [4/4] Starting RAG Chatbot server...
echo.
echo ============================================================
echo   Server starting...
echo.
echo   API URL: http://localhost:8000
echo   Health:  http://localhost:8000/health
echo   Docs:    http://localhost:8000/docs
echo.
echo   Press Ctrl+C to stop the server
echo ============================================================
echo.

cd backend
python main_simple.py
