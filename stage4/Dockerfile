# Dockerfile for Sales Forecasting Application
# Using slim-bullseye for better package availability
FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies and build tools in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Upgrade pip and setup tools
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements and install in stages for better caching
COPY requirements.txt .

# Install core dependencies first (most stable, cache-friendly)
RUN pip install --no-cache-dir --timeout 1000 \
    numpy>=1.24.0 \
    pandas>=2.0.0 \
    scikit-learn>=1.3.0

# Install web frameworks (lighter packages)
RUN pip install --no-cache-dir --timeout 1000 \
    fastapi>=0.104.0 \
    uvicorn[standard]>=0.24.0 \
    pydantic>=2.0.0 \
    streamlit>=1.28.0

# Install visualization packages
RUN pip install --no-cache-dir --timeout 1000 \
    plotly>=5.18.0 \
    matplotlib>=3.8.0 \
    seaborn>=0.13.0

# Install remaining packages
RUN pip install --no-cache-dir --timeout 1000 \
    mlflow>=2.8.0 \
    scipy>=1.11.0 \
    python-dateutil>=2.8.0 \
    python-multipart>=0.0.6 \
    psutil>=5.9.0 \
    python-dotenv>=1.0.0 \
    pyyaml>=6.0.0

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
