# 🚀 Walmart Sales Forecasting - Deployment & Usage Guide

## ✅ Current Status

Your project is **fully deployed and ready to use!**

- ✅ Model trained: Random Forest (99.96% R² accuracy)
- ✅ Dashboard running: http://localhost:8501
- ✅ 50,000 historical records loaded for predictions
- ✅ All 4 stages completed (Data → Analysis → ML → Deployment)

---

## 📊 Option 1: Interactive Dashboard (RECOMMENDED)

### Access the Dashboard

Open your browser and go to:

```
http://localhost:8501
```

### Dashboard Features

#### 🔮 Make Predictions Tab

**Single Prediction:**

1. Enter store details (Store #, Dept, Date)
2. Set conditions (Temperature, Holiday, etc.)
3. Click "🔮 Predict"
4. See prediction with confidence interval

**Multi-Week Forecast:**

1. Select Store and Department
2. Choose start date and number of weeks
3. Get weekly forecasts with trend visualization

**Batch Predictions:**

1. Upload CSV file with multiple rows
2. Get predictions for all at once

#### 📈 Model Performance Tab

- View accuracy metrics (MAE, RMSE, R²)
- See model training history
- Confidence intervals

#### 🔍 Monitoring Tab

- Performance tracking over time
- Data drift detection
- Prediction logs

#### ℹ️ Model Info Tab

- Feature importance
- Model specifications
- Training details

---

## 🔧 Option 2: REST API

### Start the API Server

```powershell
cd stage4
python run_api.py
```

The API will be available at: `http://localhost:8000`

### API Documentation

Open in browser: `http://localhost:8000/docs`

### API Endpoints

#### 1. Single Prediction

```bash
POST http://localhost:8000/predict
Content-Type: application/json

{
  "Store": 2,
  "Dept": 1,
  "Date": "2012-11-23",
  "Type": "A",
  "Size": 150000,
  "IsHoliday": true,
  "Temperature": 54.0,
  "Fuel_Price": 3.51,
  "CPI": 211.0,
  "Unemployment": 7.5
}
```

#### 2. Batch Predictions

```bash
POST http://localhost:8000/predict/batch
Content-Type: application/json

{
  "predictions": [
    { "Store": 1, "Dept": 1, "Date": "2012-11-23", ... },
    { "Store": 2, "Dept": 5, "Date": "2012-11-23", ... }
  ]
}
```

#### 3. Multi-Week Forecast

```bash
GET http://localhost:8000/predict/week?store=1&dept=1&start_date=2012-11-01&weeks=4
```

#### 4. Health Check

```bash
GET http://localhost:8000/health
```

#### 5. Model Info

```bash
GET http://localhost:8000/model/info
```

---

## 🐳 Option 3: Docker Deployment

### Build and Run with Docker Compose

```powershell
cd stage4
docker-compose up -d
```

This starts 3 services:

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **MLflow**: http://localhost:5000

### Stop Services

```powershell
docker-compose down
```

---

## 💻 Option 4: Python Code Integration

### Use the Predictor Directly

```python
from deployment.predictor import SalesPredictor

# Initialize predictor
predictor = SalesPredictor()

# Make a single prediction
input_data = {
    'Store': 2,
    'Dept': 1,
    'Date': '2012-11-23',
    'Type': 'A',
    'Size': 150000,
    'IsHoliday': True,
    'Temperature': 54.0,
    'Fuel_Price': 3.51,
    'CPI': 211.0,
    'Unemployment': 7.5
}

result = predictor.predict_single(input_data)
print(f"Predicted Sales: ${result['predicted_sales']:,.2f}")
print(f"Confidence Interval: ${result['ci_lower']:,.2f} - ${result['ci_upper']:,.2f}")

# Multi-week forecast
predictions = predictor.predict_multi_week(
    store=2,
    dept=1,
    start_date='2012-11-01',
    weeks=4
)
```

---

## 🎯 Tips for Best Predictions

Based on feature importance analysis:

### Features That Matter Most (Change these for big variations):

1. **Day of Week (22.71% impact)**

   - Weekends show different patterns than weekdays
   - Try dates on Saturday/Sunday vs Monday

2. **Month/Season (8.01% impact)**

   - Holiday months (Nov/Dec) have higher sales
   - Summer months show different patterns

3. **Store Size (7.54% impact)**

   - Larger stores (200K+ sq ft) → Higher sales
   - Smaller stores (100K sq ft) → Lower sales

4. **Promotions/Markdowns (22.61% combined)**

   - Active markdowns significantly boost predictions
   - Try with/without markdown values

5. **Historical Patterns (14.07%)**
   - Each Store/Dept has unique history
   - Different combinations give varied predictions

### Test Examples:

**High Sales Scenario:**

- Large Type A store (200K+ sq ft)
- Department with high historical sales
- Holiday week (Thanksgiving, Christmas)
- Weekend date
- Active promotions

**Low Sales Scenario:**

- Small Type C store (100K sq ft)
- Weekday in summer
- No holiday
- No promotions

---

## 📊 Monitoring & Performance

### Check Prediction Logs

```powershell
cd stage4/monitoring/logs
Get-Content predictions.jsonl -Tail 10
```

### View Performance Metrics

```python
from monitoring.performance_tracker import PerformanceTracker

tracker = PerformanceTracker()
metrics = tracker.calculate_metrics(days=7)
print(metrics)
```

### Detect Data Drift

```python
from monitoring.drift_detector import DriftDetector

detector = DriftDetector()
results = detector.detect_all_features(current_data, reference_data)
```

---

## 🔄 Re-training the Model

If you need to retrain with new data:

```powershell
# Step 1: Update data in datasets/
# Step 2: Run stage1 pipeline
cd stage1
python Stage1_pipline_runner.py

# Step 3: Run stage2 pipeline
cd ../stage2
python Stage2_pipline_runner.py

# Step 4: Train new model
cd ../stage3/ML_models
python Best_model.py

# Step 5: Copy model to deployment
Copy-Item "best_rf_model.pkl" -Destination "../../stage4/models/best_model.pkl" -Force

# Step 6: Restart dashboard
cd ../../stage4
python run_dashboard.py
```

---

## 🐛 Troubleshooting

### Dashboard won't start

```powershell
# Kill existing process
Get-Process | Where-Object {$_.ProcessName -like "*streamlit*"} | Stop-Process

# Restart
cd stage4
python run_dashboard.py
```

### Model not loading

```powershell
# Check if model exists
Test-Path stage4/models/best_model.pkl

# If not, train it
cd stage3/ML_models
python Best_model.py
Copy-Item "best_rf_model.pkl" -Destination "../../stage4/models/best_model.pkl"
```

### Predictions not varying

- Clear browser cache (Ctrl + Shift + R)
- Try very different inputs (different stores, dates, sizes)
- Check terminal output for debug logs

---

## 📁 Project Structure

```
stage4/
├── deployment/          # API and prediction logic
│   ├── api.py          # FastAPI REST endpoints
│   ├── predictor.py    # Model inference
│   └── config.py       # Configuration
├── dashboard/          # Streamlit UI
│   └── app.py         # Interactive dashboard
├── monitoring/         # Performance tracking
│   ├── performance_tracker.py
│   └── drift_detector.py
├── mlops/             # MLflow integration
│   ├── mlflow_tracking.py
│   └── model_registry.py
├── models/            # Trained models
│   └── best_model.pkl # Production model (99.96% R²)
├── run_dashboard.py   # Start dashboard
├── run_api.py         # Start API
└── docker-compose.yml # Container orchestration
```

---

## 🎓 Next Steps

### For Production Deployment:

1. **Cloud Hosting**: Deploy to Azure/AWS/GCP
2. **Authentication**: Add API keys/OAuth
3. **Scaling**: Use Kubernetes for scaling
4. **CI/CD**: Automate deployment pipeline
5. **Monitoring**: Set up alerts and logging

### For Improvement:

1. **More Data**: Retrain with recent data
2. **New Features**: Add weather, events, competition data
3. **Deep Learning**: Try LSTM/Transformer models
4. **A/B Testing**: Compare model versions

---

## 📞 Support & Documentation

- **Stage 4 README**: `stage4/README.md`
- **Stage 5 Report**: `stage5/Final_Report/Final_Project_Report.md`
- **Presentation**: `stage5/Presentation/Stakeholder_Presentation.md`
- **Quick Start**: `QUICK_START_GUIDE.md`

---

## ✅ You're All Set!

Your model is deployed and ready to use! 🎉

**Current Status:**

- ✅ Dashboard running at http://localhost:8501
- ✅ Model loaded (99.96% accuracy)
- ✅ 50,000 historical records available
- ✅ All features working

**Start using it now!** Open http://localhost:8501 in your browser! 🚀
