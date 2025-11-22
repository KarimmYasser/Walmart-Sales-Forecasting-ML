#!/usr/bin/env pwsh
# Docker Test Script for Sales Forecasting Application
# This script tests the Docker setup and verifies all services are working

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Docker Setup Verification" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed and running
Write-Host "[1/7] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[2/7] Checking Docker daemon..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker daemon is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker daemon is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[3/7] Verifying required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "docker-compose.yml",
    "Dockerfile",
    "requirements.txt",
    "deployment/api.py",
    "deployment/predictor.py",
    "deployment/config.py",
    "dashboard/app.py",
    "models/best_model.pkl"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (missing)" -ForegroundColor Red
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "✗ Missing files detected. Please ensure all required files exist." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[4/7] Checking stage3 dependencies..." -ForegroundColor Yellow
if (Test-Path "../stage3/ML_models/Feature_Engineering.py") {
    Write-Host "✓ stage3/ML_models directory accessible" -ForegroundColor Green
} else {
    Write-Host "✗ stage3/ML_models directory not found" -ForegroundColor Red
    Write-Host "  This is required for Feature_Engineering imports" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "[5/7] Building Docker images..." -ForegroundColor Yellow
Write-Host "This may take a few minutes on first run..." -ForegroundColor Cyan
docker-compose build --no-cache
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Docker images built successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Docker build failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[6/7] Starting Docker containers..." -ForegroundColor Yellow
docker-compose up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Containers started successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to start containers" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[7/7] Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Testing Services" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Test API Health
Write-Host "Testing API health endpoint..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ API is healthy (http://localhost:8000)" -ForegroundColor Green
    } else {
        Write-Host "✗ API returned status code: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "✗ API is not responding" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Testing Streamlit dashboard..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8501" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Dashboard is running (http://localhost:8501)" -ForegroundColor Green
    } else {
        Write-Host "✗ Dashboard returned status code: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠ Dashboard may still be initializing..." -ForegroundColor Yellow
    Write-Host "  This is normal for first run. Check manually in 30 seconds." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Testing MLflow server..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -UseBasicParsing -TimeoutSec 10
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ MLflow is running (http://localhost:5000)" -ForegroundColor Green
    } else {
        Write-Host "✗ MLflow returned status code: $($response.StatusCode)" -ForegroundColor Red
    }
} catch {
    Write-Host "⚠ MLflow may still be initializing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Container Status" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Access Points" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "📊 Dashboard:    http://localhost:8501" -ForegroundColor Cyan
Write-Host "🔌 API:          http://localhost:8000" -ForegroundColor Cyan
Write-Host "📖 API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "🧪 MLflow:       http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Useful Commands" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "View logs:       docker-compose logs -f" -ForegroundColor Yellow
Write-Host "Stop services:   docker-compose down" -ForegroundColor Yellow
Write-Host "Restart:         docker-compose restart" -ForegroundColor Yellow
Write-Host "Rebuild:         docker-compose up -d --build" -ForegroundColor Yellow
Write-Host ""
Write-Host "✓ Docker setup verification complete!" -ForegroundColor Green
