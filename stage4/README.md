# Stage 4: MLOps, Deployment, and Monitoring

## 📋 Overview

This stage implements MLOps practices, deploys the sales forecasting model, and sets up monitoring infrastructure for production use.

## 🎯 Milestone 4 Objectives

- ✅ Implement MLOps with experiment tracking (MLflow)
- ✅ Deploy model as REST API (FastAPI)
- ✅ Create interactive dashboard (Streamlit)
- ✅ Set up model monitoring and drift detection
- ✅ Containerize application with Docker

---

## 📁 Directory Structure

```
stage4/
│
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Multi-container orchestration
├── Dockerfile                     # Container image definition
│
├── mlops/                         # MLOps & Experiment Tracking
│   ├── mlflow_tracking.py         # MLflow experiment logging
│   ├── model_registry.py          # Model versioning & registry
│   └── experiment_runner.py       # Automated experiment execution
│
├── deployment/                    # Model Deployment
│   ├── api.py                     # FastAPI REST service
│   ├── predictor.py               # Prediction logic
│   └── config.py                  # API configuration
│
├── dashboard/                     # Interactive Dashboard
│   ├── app.py                     # Streamlit application
│   ├── components/                # UI components
│   │   ├── prediction_ui.py       # Prediction interface
│   │   ├── monitoring_ui.py       # Monitoring dashboard
│   │   └── visualizations.py      # Chart components
│   └── utils.py                   # Helper functions
│
├── monitoring/                    # Model Monitoring
│   ├── performance_tracker.py     # Performance metrics tracking
│   ├── drift_detector.py          # Data/concept drift detection
│   ├── alerting.py                # Alert system
│   └── retraining_scheduler.py    # Automated retraining logic
│
└── models/                        # Saved Models
    ├── best_model.pkl             # Production model
    ├── model_metadata.json        # Model information
    └── feature_config.json        # Feature configurations
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Train and Log Model with MLflow

```bash
# Run MLflow experiment
python mlops/experiment_runner.py

# Start MLflow UI
mlflow ui --port 5000
# Visit: http://localhost:5000
```

### 3. Deploy API

```bash
# Start FastAPI server
uvicorn deployment.api:app --reload --port 8000

# API Documentation: http://localhost:8000/docs
```

### 4. Launch Dashboard

```bash
# Start Streamlit dashboard
streamlit run dashboard/app.py

# Visit: http://localhost:8501
```

### 5. Docker Deployment

```bash
# Build and run all services
docker-compose up --build

# Services:
# - API: http://localhost:8000
# - Dashboard: http://localhost:8501
# - MLflow: http://localhost:5000
```

---

## 🔧 Components

### 1. MLOps & Experiment Tracking

**Purpose:** Track experiments, versions, and model lineage

**Features:**

- Automated experiment logging with MLflow
- Parameter, metric, and artifact tracking
- Model versioning and registry
- Reproducible experiment runs
- Model comparison tools

**Usage:**

```python
from mlops.mlflow_tracking import MLflowTracker

tracker = MLflowTracker(experiment_name="sales_forecasting")
tracker.log_model_training(model, metrics, params, features)
```

### 2. Model Deployment API

**Purpose:** Serve predictions via REST API

**Endpoints:**

- `POST /predict` - Single prediction
- `POST /predict/batch` - Batch predictions
- `GET /health` - Service health check
- `GET /model/info` - Model metadata

**Example Request:**

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Store": 1,
    "Dept": 1,
    "Date": "2023-11-22",
    "IsHoliday": false,
    "Temperature": 42.31,
    "Fuel_Price": 2.572,
    "Type": "A"
  }'
```

### 3. Interactive Dashboard

**Purpose:** User-friendly interface for predictions and monitoring

**Features:**

- Real-time sales predictions
- Historical performance analysis
- Model metrics visualization
- Feature importance display
- Data drift monitoring
- Interactive charts and filters

### 4. Model Monitoring

**Purpose:** Track model performance and detect issues

**Features:**

- Performance metric tracking over time
- Data drift detection (feature distributions)
- Concept drift detection (prediction accuracy)
- Automated alerting for performance degradation
- Retraining triggers and scheduling

**Metrics Monitored:**

- MAE, RMSE, R² score
- Prediction distribution shifts
- Feature value distributions
- API response times
- Error rates

---

## 📊 Monitoring & Alerts

### Performance Degradation Alerts

System triggers alerts when:

- R² score drops below 0.90 (from 0.9996 baseline)
- MAE increases above $500 (from $106.77 baseline)
- Feature drift detected (KS test p-value < 0.05)
- Prediction anomalies (outliers > 3 std dev)

### Retraining Strategy

**Automatic Retraining Triggers:**

1. **Scheduled:** Monthly retraining with new data
2. **Performance-Based:** When R² < 0.90 for 7 days
3. **Drift-Based:** When feature drift detected in 3+ features
4. **Manual:** On-demand via dashboard or API

---

## 🐳 Docker Deployment

### Services

1. **API Service** (Port 8000)

   - FastAPI application
   - Model inference
   - Health checks

2. **Dashboard** (Port 8501)

   - Streamlit UI
   - Interactive visualizations
   - Monitoring interface

3. **MLflow Server** (Port 5000)
   - Experiment tracking
   - Model registry
   - Artifact storage

### Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild
docker-compose up --build
```

---

## 📈 Model Performance (Production)

| Metric             | Value         | Status       |
| ------------------ | ------------- | ------------ |
| **R² Score**       | 0.9996        | ✅ Excellent |
| **MAE**            | $106.77       | ✅ Excellent |
| **RMSE**           | $144.53       | ✅ Excellent |
| **Model Type**     | Random Forest | -            |
| **Features**       | 44 engineered | -            |
| **Training Time**  | ~2 minutes    | -            |
| **Inference Time** | <10ms         | ✅ Fast      |

---

## 🔐 Security Considerations

- API authentication (API keys)
- Input validation and sanitization
- Rate limiting
- HTTPS in production
- Environment variable management
- Secret management (AWS Secrets Manager, Azure Key Vault)

---

## 📝 Deliverables

### ✅ Completed

1. **Deployed Model** - FastAPI REST API serving predictions
2. **MLOps Pipeline** - MLflow experiment tracking and model registry
3. **Interactive Dashboard** - Streamlit application for users
4. **Monitoring System** - Performance tracking and drift detection
5. **Docker Containerization** - Production-ready containers
6. **MLOps Report** - Comprehensive documentation

---

## 🔮 Next Steps (Stage 5)

1. Final project documentation
2. Business impact analysis
3. Stakeholder presentation
4. Future improvements roadmap

---

## 👥 Support

For questions or issues:

- Review documentation in each component directory
- Check MLflow UI for experiment history
- Review API logs for debugging
- Monitor dashboard alerts

---

**Status:** ✅ Milestone 4 Complete - Production Ready
