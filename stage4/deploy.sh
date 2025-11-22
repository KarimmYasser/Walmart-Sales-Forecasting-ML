#!/bin/bash

# Quick Deployment Script for Walmart Sales Forecasting
# Run this script on your cloud server after cloning the repository

set -e  # Exit on error

echo "======================================"
echo "Walmart Sales Forecasting Deployment"
echo "======================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}→ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run with sudo: sudo ./deploy.sh"
    exit 1
fi

# Get non-root user
REAL_USER=${SUDO_USER:-$USER}
REAL_HOME=$(eval echo ~$REAL_USER)

echo "Step 1: Installing Docker..."
if ! command -v docker &> /dev/null; then
    print_info "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    usermod -aG docker $REAL_USER
    print_success "Docker installed"
else
    print_success "Docker already installed"
fi

echo ""
echo "Step 2: Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    print_info "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    print_success "Docker Compose installed"
else
    print_success "Docker Compose already installed"
fi

echo ""
echo "Step 3: Setting up firewall..."
if command -v ufw &> /dev/null; then
    print_info "Configuring UFW firewall..."
    ufw --force enable
    ufw allow OpenSSH
    ufw allow 80/tcp
    ufw allow 443/tcp
    print_success "Firewall configured"
else
    print_info "UFW not installed, skipping firewall setup"
fi

echo ""
echo "Step 4: Creating necessary directories..."
cd $REAL_HOME/Depi_project_Data-science/stage4
mkdir -p models mlruns logs
chown -R $REAL_USER:$REAL_USER models mlruns logs
print_success "Directories created"

echo ""
echo "Step 5: Building and starting containers..."
print_info "This may take 5-10 minutes..."
su - $REAL_USER -c "cd $REAL_HOME/Depi_project_Data-science/stage4 && docker-compose -f docker-compose.production.yml up --build -d"
print_success "Containers started"

echo ""
echo "Step 6: Waiting for services to be ready..."
sleep 10

# Check if containers are running
if docker ps | grep -q "sales_forecast"; then
    print_success "All containers are running!"
else
    print_error "Some containers failed to start. Check logs with: docker-compose -f docker-compose.production.yml logs"
    exit 1
fi

# Get server IP
SERVER_IP=$(curl -s ifconfig.me)

echo ""
echo "======================================"
echo "✓ DEPLOYMENT COMPLETE!"
echo "======================================"
echo ""
echo "Your application is now live at:"
echo ""
echo "  Dashboard: http://$SERVER_IP/"
echo "  API:       http://$SERVER_IP/api/"
echo "  API Docs:  http://$SERVER_IP/api/docs"
echo ""
echo "Useful commands:"
echo "  - View logs:    docker-compose -f docker-compose.production.yml logs -f"
echo "  - Stop:         docker-compose -f docker-compose.production.yml stop"
echo "  - Restart:      docker-compose -f docker-compose.production.yml restart"
echo "  - Update:       git pull && docker-compose -f docker-compose.production.yml up --build -d"
echo ""
echo "Next steps:"
echo "  1. Configure your domain name (if you have one)"
echo "  2. Set up SSL certificate: sudo certbot --nginx -d your-domain.com"
echo "  3. Set up monitoring and alerts"
echo ""
echo "======================================"
