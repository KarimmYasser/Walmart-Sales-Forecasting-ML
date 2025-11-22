# 🌐 Cloud Deployment Guide - Walmart Sales Forecasting

Complete guide for deploying the sales forecasting system to a cloud server with both API and Dashboard accessible on the same domain.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Quick Deploy (Any Cloud VM)](#quick-deploy-any-cloud-vm)
3. [Azure Deployment](#azure-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Google Cloud Deployment](#google-cloud-deployment)
6. [Post-Deployment](#post-deployment)
7. [Monitoring & Maintenance](#monitoring--maintenance)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- Cloud account (Azure/AWS/GCP or any VPS provider)
- Domain name (optional but recommended)
- Git installed on your local machine
- Docker installed (for containerized deployment)

### Server Requirements

- **Minimum**: 2 vCPU, 4GB RAM, 20GB disk
- **Recommended**: 4 vCPU, 8GB RAM, 50GB disk
- OS: Ubuntu 20.04/22.04 or similar Linux distribution

---

## Quick Deploy (Any Cloud VM)

This method works on **any cloud provider** (Azure, AWS, GCP, DigitalOcean, Linode, etc.)

### Step 1: Get a Server

**Option A: Azure VM**

```bash
# Create resource group
az group create --name walmart-forecast-rg --location eastus

# Create VM
az vm create \
  --resource-group walmart-forecast-rg \
  --name forecast-server \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# Open ports
az vm open-port --port 80 --resource-group walmart-forecast-rg --name forecast-server
az vm open-port --port 443 --resource-group walmart-forecast-rg --name forecast-server
```

**Option B: AWS EC2**

```bash
# Launch EC2 instance (t3.medium, Ubuntu 22.04)
# Open ports 80, 443 in Security Group
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip
```

**Option C: Any VPS Provider**

- Create Ubuntu 20.04/22.04 server (2+ CPU, 4+ GB RAM)
- Ensure ports 80 and 443 are open
- Get the server's public IP address

### Step 2: Connect to Server

```bash
# SSH into your server
ssh your-username@your-server-ip

# Update system
sudo apt update && sudo apt upgrade -y
```

### Step 3: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker-compose --version
```

### Step 4: Clone and Deploy Project

```bash
# Clone repository
git clone https://github.com/ahmedhaithamamer/Depi_project_Data-science.git
cd Depi_project_Data-science/stage4

# Create necessary directories
mkdir -p models mlruns

# Copy trained model (if not in repo)
# You may need to upload best_model.pkl to models/ directory
# scp stage4/models/best_model.pkl your-username@your-server-ip:~/Depi_project_Data-science/stage4/models/

# Build and start services
docker-compose -f docker-compose.production.yml up --build -d

# Check status
docker-compose -f docker-compose.production.yml ps
```

### Step 5: Configure Domain (Optional)

If you have a domain name:

```bash
# Edit nginx.conf
nano nginx.conf

# Change this line:
server_name _;

# To:
server_name your-domain.com www.your-domain.com;
```

Then update your domain's DNS records:

- **A Record**: Point to your server's IP address
- **CNAME**: `www` → your-domain.com

Wait 5-10 minutes for DNS propagation, then restart:

```bash
docker-compose -f docker-compose.production.yml restart nginx
```

### Step 6: Access Your Deployment

**Using IP Address:**

- Dashboard: `http://YOUR-SERVER-IP/`
- API: `http://YOUR-SERVER-IP/api/`
- API Docs: `http://YOUR-SERVER-IP/api/docs`

**Using Domain Name:**

- Dashboard: `http://your-domain.com/`
- API: `http://your-domain.com/api/`
- API Docs: `http://your-domain.com/api/docs`

---

## Azure Deployment

### Method 1: Azure Container Instances (Fastest)

```bash
# Login to Azure
az login

# Create resource group
az group create --name walmart-forecast-rg --location eastus

# Create container registry
az acr create --resource-group walmart-forecast-rg \
  --name walmartforecastacr --sku Basic

# Build and push images
az acr build --registry walmartforecastacr \
  --image sales-forecast:latest .

# Deploy container group with both services
az container create \
  --resource-group walmart-forecast-rg \
  --name forecast-container \
  --image walmartforecastacr.azurecr.io/sales-forecast:latest \
  --dns-name-label walmart-forecast-app \
  --ports 80 443

# Get FQDN
az container show --resource-group walmart-forecast-rg \
  --name forecast-container \
  --query ipAddress.fqdn --output tsv
```

Access at: `http://<your-dns-label>.eastus.azurecontainer.io/`

### Method 2: Azure App Service (Recommended for Production)

```bash
# Create App Service Plan
az appservice plan create \
  --name forecast-plan \
  --resource-group walmart-forecast-rg \
  --sku B2 --is-linux

# Create Web App for Dashboard
az webapp create \
  --resource-group walmart-forecast-rg \
  --plan forecast-plan \
  --name walmart-forecast-dashboard \
  --deployment-container-image-name walmartforecastacr.azurecr.io/sales-forecast:latest

# Create Web App for API
az webapp create \
  --resource-group walmart-forecast-rg \
  --plan forecast-plan \
  --name walmart-forecast-api \
  --deployment-container-image-name walmartforecastacr.azurecr.io/sales-forecast:latest

# Configure API
az webapp config appsettings set \
  --resource-group walmart-forecast-rg \
  --name walmart-forecast-api \
  --settings WEBSITES_PORT=8000

# Configure Dashboard
az webapp config appsettings set \
  --resource-group walmart-forecast-rg \
  --name walmart-forecast-dashboard \
  --settings WEBSITES_PORT=8501
```

Access:

- Dashboard: `https://walmart-forecast-dashboard.azurewebsites.net/`
- API: `https://walmart-forecast-api.azurewebsites.net/`

---

## AWS Deployment

### Method 1: AWS Elastic Beanstalk

```bash
# Install EB CLI
pip install awsebcli

# Initialize EB application
cd stage4
eb init -p docker walmart-sales-forecast --region us-east-1

# Create environment
eb create forecast-prod --instance-type t3.medium

# Deploy
eb deploy

# Open in browser
eb open
```

### Method 2: AWS ECS (Fargate)

See detailed guide in `AWS_DEPLOYMENT.md` (create this file separately if needed)

---

## Google Cloud Deployment

### Cloud Run (Serverless)

```bash
# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR-PROJECT-ID

# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/sales-forecast

# Deploy API
gcloud run deploy sales-forecast-api \
  --image gcr.io/YOUR-PROJECT-ID/sales-forecast \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 2Gi

# Deploy Dashboard
gcloud run deploy sales-forecast-dashboard \
  --image gcr.io/YOUR-PROJECT-ID/sales-forecast \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8501 \
  --memory 2Gi
```

---

## Post-Deployment

### 1. Enable HTTPS (Recommended)

**Using Let's Encrypt (Free SSL):**

```bash
# SSH into server
ssh your-username@your-server-ip

# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal (already configured by certbot)
sudo certbot renew --dry-run
```

**Update nginx.conf for HTTPS:**
The certbot command will automatically update your nginx configuration.

### 2. Set Up Firewall

```bash
# Enable UFW
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable

# Check status
sudo ufw status
```

### 3. Configure Environment Variables

```bash
# Create .env file
cat > .env << EOF
MODEL_PATH=/app/models/best_model.pkl
API_URL=http://api:8000
PYTHONUNBUFFERED=1
# Add any API keys or secrets here
EOF

# Update docker-compose.production.yml to use .env
```

### 4. Set Up Monitoring

```bash
# Install monitoring tools
docker run -d \
  --name=grafana \
  -p 3000:3000 \
  grafana/grafana

# Access Grafana at http://your-ip:3000
# Default login: admin/admin
```

---

## Monitoring & Maintenance

### View Logs

```bash
# All services
docker-compose -f docker-compose.production.yml logs

# Specific service
docker-compose -f docker-compose.production.yml logs api
docker-compose -f docker-compose.production.yml logs dashboard

# Follow logs in real-time
docker-compose -f docker-compose.production.yml logs -f
```

### Check Container Status

```bash
# List running containers
docker-compose -f docker-compose.production.yml ps

# Check resource usage
docker stats
```

### Update Deployment

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.production.yml up --build -d

# Or specific service
docker-compose -f docker-compose.production.yml up --build -d api
```

### Backup Model and Data

```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz models/ mlruns/ datasets/
echo "Backup created: backup_$DATE.tar.gz"
EOF

chmod +x backup.sh

# Schedule daily backup (cron)
(crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup.sh") | crontab -
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose -f docker-compose.production.yml logs api

# Check if ports are in use
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :8000

# Restart specific service
docker-compose -f docker-compose.production.yml restart api
```

### Out of Memory

```bash
# Check memory usage
free -h
docker stats

# Increase swap (if needed)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Cannot Access Dashboard

1. Check if container is running: `docker ps`
2. Check nginx logs: `docker logs sales_forecast_nginx`
3. Verify firewall: `sudo ufw status`
4. Test internal connection: `curl http://localhost:8501`

### Model Not Found

```bash
# Check if model exists
docker exec sales_forecast_api ls -la /app/models/

# Copy model to container
docker cp stage3/ML_models/best_rf_model.pkl sales_forecast_api:/app/models/best_model.pkl

# Restart API
docker-compose -f docker-compose.production.yml restart api
```

---

## Performance Optimization

### 1. Enable Caching

Add Redis for prediction caching:

```yaml
# Add to docker-compose.production.yml
redis:
  image: redis:alpine
  container_name: sales_forecast_redis
  networks:
    - sales_forecast_network
```

### 2. Scale Services

```bash
# Scale API to 3 instances
docker-compose -f docker-compose.production.yml up -d --scale api=3
```

### 3. Use CDN

For static assets, configure a CDN like Cloudflare.

---

## Security Checklist

- [ ] Enable HTTPS with valid SSL certificate
- [ ] Set up firewall (UFW/Security Groups)
- [ ] Use strong passwords/SSH keys
- [ ] Keep system updated: `sudo apt update && sudo apt upgrade`
- [ ] Enable automatic security updates
- [ ] Set up fail2ban for SSH protection
- [ ] Use environment variables for secrets
- [ ] Enable Docker security scanning
- [ ] Set up regular backups
- [ ] Configure rate limiting in nginx

---

## Cost Estimation

### Cloud Provider Costs (Monthly)

| Provider         | Configuration                 | Estimated Cost |
| ---------------- | ----------------------------- | -------------- |
| **Azure VM**     | Standard_D2s_v3 (2 vCPU, 8GB) | ~$70-90/month  |
| **AWS EC2**      | t3.medium (2 vCPU, 4GB)       | ~$30-40/month  |
| **GCP VM**       | e2-medium (2 vCPU, 4GB)       | ~$25-35/month  |
| **DigitalOcean** | 2 vCPU, 4GB RAM droplet       | $24/month      |
| **Linode**       | 2 vCPU, 4GB RAM               | $24/month      |

_Note: Add ~$10-15/month for load balancer/domain if needed_

---

## Next Steps

1. ✅ Deploy to server
2. ✅ Configure domain and SSL
3. ✅ Set up monitoring
4. 📊 Configure analytics (Google Analytics, etc.)
5. 🔔 Set up alerts (email notifications for errors)
6. 📈 Implement auto-scaling (if needed)
7. 🔒 Implement authentication (if needed)
8. 📱 Create mobile-responsive dashboard views

---

## Support

For issues or questions:

- GitHub: https://github.com/ahmedhaithamamer/Depi_project_Data-science
- Check logs: `docker-compose logs`
- Review documentation: `DEPLOYMENT_GUIDE.md`

---

**🎉 Your Walmart Sales Forecasting system is now live!**

Dashboard: `http://your-domain.com/`  
API: `http://your-domain.com/api/`  
API Docs: `http://your-domain.com/api/docs`
