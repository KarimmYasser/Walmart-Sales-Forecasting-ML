# Quick Run Guide

## Running the Services

### Option 1: Using Helper Scripts (Recommended)

```bash
# From stage4 directory

# Run Dashboard
python run_dashboard.py

# Run API (in another terminal)
python run_api.py
```

### Option 2: Direct Commands

```bash
# Run Dashboard
streamlit run dashboard/app.py

# Run API
uvicorn deployment.api:app --reload --port 8000
```

### Option 3: Docker (Best for Production)

```bash
# Start all services
docker-compose up --build

# Services available at:
# - API: http://localhost:8000/docs
# - Dashboard: http://localhost:8501
# - MLflow: http://localhost:5000
```

## Troubleshooting Import Warnings

The import warnings you saw are from the Python language server and won't affect runtime. The code includes:

1. **`__init__.py` files** - Makes directories proper Python packages
2. **Dynamic path management** - Adds paths at runtime
3. **Error handling** - Catches import errors gracefully
4. **Helper scripts** - Ensure correct working directory

### If imports still fail at runtime:

```bash
# Make sure you're in the stage4 directory
cd stage4

# Install all dependencies
pip install -r requirements.txt

# Use the helper scripts
python run_dashboard.py
```

## Running from VS Code

1. Open terminal in VS Code
2. Navigate to stage4: `cd stage4`
3. Run: `python run_dashboard.py`

The warnings in the editor are static analysis warnings and won't affect execution.
