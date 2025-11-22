# Docker Deployment - Quick Reference

## ✅ Prerequisites Checklist

Before running Docker, ensure:

- [ ] Docker Desktop installed and running
- [ ] All files present in stage4/
- [ ] Model file exists: `stage4/models/best_model.pkl`
- [ ] stage3/ML_models accessible (for Feature_Engineering)
- [ ] Current directory is `stage4/`

## 🚀 Quick Start (3 Commands)

```bash
# 1. Navigate to stage4 directory
cd stage4

# 2. Build and start all services
docker-compose up -d --build

# 3. Access services
# - Dashboard: http://localhost:8501
# - API: http://localhost:8000/docs
# - MLflow: http://localhost:5000
```

## 🧪 Test Docker Setup

Run the automated test script:

```powershell
# Windows PowerShell
cd stage4
.\test_docker.ps1
```

This script will:

1. ✓ Verify Docker installation
2. ✓ Check required files
3. ✓ Build Docker images
4. ✓ Start containers
5. ✓ Test all services
6. ✓ Show access points

## 🐳 Docker Commands Reference

### Start Services

```bash
docker-compose up -d                    # Start in background
docker-compose up                       # Start with logs visible
docker-compose up -d --build            # Rebuild and start
```

### Check Status

```bash
docker-compose ps                       # List running containers
docker-compose logs                     # View all logs
docker-compose logs -f api              # Follow API logs
docker-compose logs -f dashboard        # Follow dashboard logs
```

### Stop Services

```bash
docker-compose stop                     # Stop containers (keep them)
docker-compose down                     # Stop and remove containers
docker-compose down -v                  # Stop, remove containers and volumes
```

### Restart Services

```bash
docker-compose restart                  # Restart all services
docker-compose restart api              # Restart only API
docker-compose restart dashboard        # Restart only dashboard
```

### Debug Commands

```bash
# Enter a running container
docker exec -it sales_forecasting_api /bin/bash
docker exec -it sales_forecasting_dashboard /bin/bash

# View container logs
docker logs sales_forecasting_api
docker logs sales_forecasting_dashboard --follow

# Inspect container
docker inspect sales_forecasting_api
```

## 📊 Service Details

### API Service (FastAPI)

- **Port**: 8000
- **Container**: `sales_forecasting_api`
- **Health Check**: `http://localhost:8000/health`
- **API Docs**: `http://localhost:8000/docs`
- **Endpoints**:
  - GET `/health` - Health check
  - POST `/predict` - Single prediction
  - POST `/predict/batch` - Batch predictions
  - POST `/predict/multi-week` - Multi-week forecast
  - GET `/model/info` - Model information
  - GET `/model/features` - Feature list

### Dashboard Service (Streamlit)

- **Port**: 8501
- **Container**: `sales_forecasting_dashboard`
- **URL**: `http://localhost:8501`
- **Features**:
  - 4 tabs: Predictions, Performance, Monitoring, Info
  - Single & multi-week forecasts
  - Model metrics visualization
  - Health & drift monitoring

### MLflow Service

- **Port**: 5000
- **Container**: `sales_forecasting_mlflow`
- **URL**: `http://localhost:5000`
- **Features**:
  - Experiment tracking
  - Model registry
  - Run comparison
  - Artifact storage

## 🔧 Configuration

### Environment Variables

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - PYTHONUNBUFFERED=1 # Real-time logging
  - PYTHONPATH=/app:/app/stage3/ML_models # Python import paths
```

### Volume Mounts

The following directories are mounted for persistence:

- `./models` → Model files
- `./monitoring/logs` → Application logs
- `./mlruns` → MLflow artifacts
- `../stage3/ML_models` → Feature Engineering code (read-only)

### Resource Limits

To add CPU/memory limits, edit `docker-compose.yml`:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: "2"
          memory: 2G
        reservations:
          cpus: "1"
          memory: 1G
```

## 🐛 Troubleshooting

### Problem: "Cannot connect to Docker daemon"

**Solution**: Start Docker Desktop

### Problem: "Port already in use"

**Solution**: Stop other services using ports 8000, 8501, or 5000

```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change ports in docker-compose.yml
ports:
  - "8080:8000"  # Use 8080 instead of 8000
```

### Problem: "Import Error: Feature_Engineering"

**Solution**: Ensure stage3/ML_models is accessible

```bash
# Check if path exists
ls ../stage3/ML_models/Feature_Engineering.py

# Verify volume mount in docker-compose.yml
volumes:
  - ../stage3/ML_models:/app/stage3/ML_models:ro
```

### Problem: "Model file not found"

**Solution**:

1. Check if model exists: `ls models/best_model.pkl`
2. If using Git LFS, pull the file: `git lfs pull`
3. Ensure volume mount is correct in docker-compose.yml

### Problem: Container keeps restarting

**Solution**: Check logs for errors

```bash
docker-compose logs api
docker-compose logs dashboard

# Check specific error
docker logs sales_forecasting_api --tail 50
```

### Problem: Dashboard shows "Connection Error"

**Solution**:

1. Ensure API container is healthy: `docker-compose ps`
2. Wait 30 seconds for full initialization
3. Check API health: `curl http://localhost:8000/health`

## 📦 Building for Production

### Production Docker Compose

Use `docker-compose.production.yml` for production:

```bash
docker-compose -f docker-compose.production.yml up -d
```

This configuration includes:

- Nginx reverse proxy
- SSL/TLS support
- Resource limits
- Health checks
- Automatic restarts
- Log rotation

### Multi-Stage Build (Optimized)

For smaller image size, use multi-stage build:

```dockerfile
# Build stage
FROM python:3.10-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "deployment.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🎯 Performance Tips

1. **Use BuildKit** for faster builds:

   ```bash
   DOCKER_BUILDKIT=1 docker-compose build
   ```

2. **Layer caching**: Don't change requirements.txt often

3. **Volume mounts**: Use for development, not production

4. **Resource allocation**: Increase Docker Desktop memory to 4GB+

5. **Image cleanup**: Remove unused images
   ```bash
   docker system prune -a
   ```

## ✅ Verification Checklist

After starting Docker, verify:

- [ ] All 3 containers running: `docker-compose ps`
- [ ] API responds: `curl http://localhost:8000/health`
- [ ] Dashboard loads: Visit `http://localhost:8501`
- [ ] MLflow accessible: Visit `http://localhost:5000`
- [ ] No errors in logs: `docker-compose logs`
- [ ] Can make predictions via API
- [ ] Dashboard shows all tabs

## 📝 Notes

- **First run**: May take 5-10 minutes to download images and build
- **Model loading**: Large model (121MB) takes ~30 seconds to load
- **Memory usage**: Expect 2-3 GB RAM usage for all services
- **Logs**: Check `monitoring/logs/` for application logs
- **Updates**: Rebuild after code changes: `docker-compose up -d --build`

## 🔗 Related Documentation

- Full deployment guide: `../DEPLOYMENT_GUIDE.md`
- Docker deployment details: `DOCKER_DEPLOYMENT.md`
- Production setup: `../CLOUD_DEPLOYMENT_GUIDE.md`
- API documentation: Available at `http://localhost:8000/docs` when running
