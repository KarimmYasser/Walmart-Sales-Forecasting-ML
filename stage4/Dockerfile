# Dockerfile for Sales Forecasting Application
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY deployment/ ./deployment/
COPY dashboard/ ./dashboard/
COPY monitoring/ ./monitoring/
COPY mlops/ ./mlops/
COPY models/ ./models/
COPY __init__.py .

# Copy helper scripts
COPY run_api.py .
COPY run_dashboard.py .

# Create necessary directories
RUN mkdir -p monitoring/logs mlruns

# Expose ports
EXPOSE 8000 8501 5000

# Default command runs the API
CMD ["python", "run_api.py"]
