@echo off
echo ========================================
echo   Physical AI Textbook - Startup
echo ========================================
echo.
echo Starting server on http://localhost:3000
echo Opening interactive textbook...
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server in the background
start "Physical AI Server" cmd /k "python -m http.server 3000"

REM Wait a moment for server to start
timeout /t 2 /nobreak >nul

REM Open the interactive textbook in default browser
start http://localhost:3000/interactive-textbook.html

echo.
echo Server started!
echo Textbook opened at: http://localhost:3000/interactive-textbook.html
echo.
echo To stop the server, close the "Physical AI Server" window
echo.
pause
