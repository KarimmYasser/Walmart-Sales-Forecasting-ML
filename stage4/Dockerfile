# Dockerfile for Sales Forecasting Application
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setup
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install Python dependencies with increased timeout
COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 1000 --retries 5 -r requirements.txt

# Copy application code
COPY deployment/ ./deployment/
COPY dashboard/ ./dashboard/
COPY monitoring/ ./monitoring/
COPY mlops/ ./mlops/
COPY models/ ./models/
COPY __init__.py .

# Create necessary directories
RUN mkdir -p monitoring/logs mlruns stage3/ML_models

# Note: stage3/ML_models will be mounted as volume at runtime
# Set Python path to include stage3
ENV PYTHONPATH=/app:/app/stage3/ML_models

# Expose ports
EXPOSE 8000 8501 5000

# Default command runs the API
CMD ["uvicorn", "deployment.api:app", "--host", "0.0.0.0", "--port", "8000"]
