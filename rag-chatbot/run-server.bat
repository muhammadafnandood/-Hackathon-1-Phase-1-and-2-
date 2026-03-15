@echo off
echo Starting RAG Chatbot Server...
cd /d "%~dp0\backend"
..\..\venv\Scripts\python main.py
pause
