@echo off
echo ========================================
echo   AI Tutor Robotics - Vercel Deploy
echo ========================================
echo.

REM Check if Node.js is installed
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found!
    echo Please install Node.js from: https://nodejs.org/
    echo.
    echo Opening Node.js download page...
    start https://nodejs.org/
    pause
    exit /b 1
)
echo OK: Node.js is installed
echo.

REM Check if Vercel CLI is installed
echo Checking Vercel CLI...
vercel --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Vercel CLI...
    npm install -g vercel
) else (
    echo OK: Vercel CLI is installed
)
echo.

REM Login to Vercel
echo ========================================
echo   Logging in to Vercel
echo ========================================
echo.
echo Please complete login in the browser...
vercel login
echo.

REM Deploy
echo ========================================
echo   Deploying to Vercel
echo ========================================
echo.
echo Deploying to production...
echo.

REM Change to project directory
cd /d "%~dp0"

REM Deploy to production
vercel --prod

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo Your app is now live!
echo Check the URL above to access your app
echo.
echo Opening Vercel dashboard...
start https://vercel.com/dashboard
echo.
pause
