# 🐳 Docker Deployment Guide

## Quick Start (3 Steps)

### 1. Build the Docker Image

```powershell
cd stage4
docker-compose build
```

### 2. Start All Services

```powershell
docker-compose up -d
```

### 3. Access Your Services

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000/docs
- **MLflow**: http://localhost:5000

---

## 🚀 Detailed Instructions

### Prerequisites

1. **Install Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop
   - Install and start Docker Desktop
   - Verify installation:
   ```powershell
   docker --version
   docker-compose --version
   ```

### Step-by-Step Deployment

#### 1. Navigate to Stage4

```powershell
cd D:\Projects\DEPI\Depi_project_Data-science\stage4
```

#### 2. Build Docker Images

```powershell
docker-compose build
```

This will:

- Download Python base image
- Install all dependencies
- Copy your application code
- Set up 3 services (API, Dashboard, MLflow)

**Expected output:**

```
[+] Building 45.2s (18/18) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 543B
 ...
Successfully built abc123def456
Successfully tagged stage4_api:latest
```

#### 3. Start All Services

```powershell
docker-compose up -d
```

The `-d` flag runs containers in the background (detached mode).

**Expected output:**

```
[+] Running 4/4
 ✔ Network stage4_sales_forecast_network  Created
 ✔ Container sales_forecasting_api        Started
 ✔ Container sales_forecasting_dashboard  Started
 ✔ Container sales_forecasting_mlflow     Started
```

#### 4. Check Services are Running

```powershell
docker-compose ps
```

**Expected output:**

```
NAME                          STATUS              PORTS
sales_forecasting_api         Up 2 minutes        0.0.0.0:8000->8000/tcp
sales_forecasting_dashboard   Up 2 minutes        0.0.0.0:8501->8501/tcp
sales_forecasting_mlflow      Up 2 minutes        0.0.0.0:5000->5000/tcp
```

#### 5. View Logs (Optional)

```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f dashboard
docker-compose logs -f mlflow
```

Press `Ctrl+C` to stop viewing logs.

---

## 🎯 Using Your Deployed Services

### 1. Interactive Dashboard

Open in browser: **http://localhost:8501**

**Features:**

- Make single predictions
- Multi-week forecasts
- Batch predictions
- Model performance metrics
- Monitoring dashboards

### 2. REST API

Open Swagger UI: **http://localhost:8000/docs**

**Test with PowerShell:**

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health"

# Make prediction
$body = @{
    Store = 2
    Dept = 1
    Date = "2012-11-23"
    Type = "A"
    Size = 150000
    IsHoliday = $true
    Temperature = 54.0
    Fuel_Price = 3.51
    CPI = 211.0
    Unemployment = 7.5
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://localhost:8000/predict" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

$result
```

### 3. MLflow Tracking

Open MLflow UI: **http://localhost:5000**

**Features:**

- View experiment runs
- Compare model versions
- Track metrics and parameters
- Model registry

---

## 🛠️ Docker Commands Reference

### Starting and Stopping

```powershell
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d api
docker-compose up -d dashboard

# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers AND volumes
docker-compose down -v
```

### Monitoring

```powershell
# Check status
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View logs (specific service)
docker-compose logs -f api

# View last 100 lines
docker-compose logs --tail=100

# Check resource usage
docker stats
```

### Rebuilding

```powershell
# Rebuild after code changes
docker-compose build

# Rebuild without cache
docker-compose build --no-cache

# Rebuild and restart
docker-compose up -d --build
```

### Accessing Containers

```powershell
# Open bash in API container
docker exec -it sales_forecasting_api bash

# Open bash in Dashboard container
docker exec -it sales_forecasting_dashboard bash

# Run Python in container
docker exec -it sales_forecasting_api python

# Check files in container
docker exec -it sales_forecasting_api ls -la
```

---

## 🔧 Troubleshooting

### Problem: Port Already in Use

**Error:**

```
Error starting userland proxy: listen tcp4 0.0.0.0:8501: bind: address already in use
```

**Solution 1:** Stop the local service

```powershell
# Find process using port 8501
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"} | Stop-Process

# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess
Stop-Process -Id <ProcessId>
```

**Solution 2:** Change ports in docker-compose.yml

```yaml
ports:
  - "8502:8501" # Changed from 8501:8501
```

### Problem: Container Keeps Restarting

**Check logs:**

```powershell
docker-compose logs api
```

**Common issues:**

- Model file missing: Ensure `models/best_model.pkl` exists
- Import errors: Rebuild with `docker-compose build --no-cache`
- Memory issues: Increase Docker memory in Docker Desktop settings

### Problem: Can't Access Services

**Check if containers are running:**

```powershell
docker-compose ps
```

**Restart services:**

```powershell
docker-compose restart
```

**Check network:**

```powershell
docker network ls
docker network inspect stage4_sales_forecast_network
```

### Problem: Changes Not Reflected

**Rebuild and restart:**

```powershell
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 📊 Production Deployment

### Environment Variables

Create `.env` file in stage4:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=false

# Model Configuration
MODEL_PATH=models/best_model.pkl

# Monitoring
LOG_LEVEL=INFO
ENABLE_METRICS=true

# Database (if needed)
DATABASE_URL=postgresql://user:pass@localhost:5432/sales_db
```

Update docker-compose.yml:

```yaml
services:
  api:
    env_file:
      - .env
```

### Scaling Services

```powershell
# Scale API to 3 instances
docker-compose up -d --scale api=3

# Use nginx for load balancing
```

### Persistent Storage

Data persists in Docker volumes:

```powershell
# List volumes
docker volume ls

# Inspect volume
docker volume inspect stage4_models

# Backup volume
docker run --rm -v stage4_models:/data -v ${PWD}:/backup alpine tar czf /backup/models-backup.tar.gz -C /data .

# Restore volume
docker run --rm -v stage4_models:/data -v ${PWD}:/backup alpine tar xzf /backup/models-backup.tar.gz -C /data
```

---

## 🚀 Cloud Deployment

### Deploy to Azure Container Instances

```powershell
# Login to Azure
az login

# Create resource group
az group create --name sales-forecasting-rg --location eastus

# Create container registry
az acr create --resource-group sales-forecasting-rg --name salesforecastacr --sku Basic

# Build and push to ACR
az acr build --registry salesforecastacr --image sales-forecast:v1 .

# Deploy to ACI
az container create \
    --resource-group sales-forecasting-rg \
    --name sales-forecast-api \
    --image salesforecastacr.azurecr.io/sales-forecast:v1 \
    --cpu 2 --memory 4 \
    --ports 8000 8501 \
    --dns-name-label sales-forecast-api
```

### Deploy to AWS ECS

```powershell
# Build and tag
docker build -t sales-forecast:latest .
docker tag sales-forecast:latest <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/sales-forecast:latest

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/sales-forecast:latest

# Deploy using ECS CLI or Console
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] All 3 containers running: `docker-compose ps`
- [ ] Dashboard accessible: http://localhost:8501
- [ ] API accessible: http://localhost:8000/docs
- [ ] Health check passes: http://localhost:8000/health
- [ ] Can make predictions through dashboard
- [ ] Can make predictions through API
- [ ] Logs are clean: `docker-compose logs`
- [ ] Model loads successfully (check logs)
- [ ] Historical data loaded (check logs)

---

## 📞 Support

If you encounter issues:

1. **Check logs**: `docker-compose logs -f`
2. **Check container status**: `docker-compose ps`
3. **Rebuild from scratch**: `docker-compose down -v && docker-compose build --no-cache && docker-compose up -d`
4. **Check Docker Desktop**: Ensure it's running and has enough resources (4GB+ RAM)

---

## 🎉 You're Done!

Your sales forecasting application is now running in Docker containers!

**Access your services:**

- 📊 Dashboard: http://localhost:8501
- 🔌 API: http://localhost:8000/docs
- 📈 MLflow: http://localhost:5000

**Stop when finished:**

```powershell
docker-compose down
```
