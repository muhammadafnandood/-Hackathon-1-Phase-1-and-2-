# Vercel Deployment Script for AI Tutor Robotics
# Run this script in PowerShell

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AI Tutor Robotics - Vercel Deploy   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found!" -ForegroundColor Red
    Write-Host "Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opening Node.js download page..." -ForegroundColor Cyan
    Start-Process "https://nodejs.org/"
    exit
}

# Check if Vercel CLI is installed
Write-Host "Checking Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version
    Write-Host "✓ Vercel CLI installed: $vercelVersion" -ForegroundColor Green
} catch {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Yellow
    npm install -g vercel
}

# Login to Vercel
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Logging in to Vercel                " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Please complete login in the browser..." -ForegroundColor Yellow
vercel login

# Deploy
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Deploying to Vercel                 " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to project directory
$projectPath = "D:\Hackathon 1"
Write-Host "Project Path: $projectPath" -ForegroundColor Yellow
Set-Location $projectPath

# Deploy to production
Write-Host "Deploying to production..." -ForegroundColor Yellow
Write-Host ""
vercel --prod

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Deployment Complete!                " -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your app is now live!" -ForegroundColor Cyan
Write-Host "Check the URL above to access your app" -ForegroundColor Yellow
Write-Host ""

# Open the deployment URL
Write-Host "Opening deployment URL..." -ForegroundColor Cyan
Start-Process "https://vercel.com/dashboard"

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
