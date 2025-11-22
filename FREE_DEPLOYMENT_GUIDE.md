# 🎓 Free Deployment Guide (Educational)

Complete guide for deploying your Walmart Sales Forecasting project **100% FREE** for educational purposes.

---

## 🆓 Best Free Options

### **Option 1: Render.com (RECOMMENDED)** ⭐

**Why:**

- ✅ 100% FREE tier (no credit card required)
- ✅ Supports Docker
- ✅ Can deploy both API and Dashboard
- ✅ 750 hours/month free (enough for educational use)
- ✅ Easy GitHub integration
- ✅ Auto-deploy on git push

**Limitations:**

- Sleeps after 15 min inactivity (wakes on first request ~30s)
- 512MB RAM per service

---

### **Option 2: Streamlit Cloud + PythonAnywhere**

**Why:**

- ✅ 100% FREE
- ✅ Dashboard on Streamlit Cloud (free)
- ✅ API on PythonAnywhere (free tier)
- ✅ Both have educational programs

**Limitations:**

- Two separate URLs
- PythonAnywhere: 100k API calls/day limit

---

### **Option 3: Hugging Face Spaces**

**Why:**

- ✅ 100% FREE
- ✅ GPU support (free tier)
- ✅ Great for ML models
- ✅ Community visibility

**Limitations:**

- Primarily for Gradio/Streamlit demos
- 16GB storage limit

---

## 🚀 Quick Start: Render.com (5 Minutes)

### Step 1: Prepare Your Repository

Your GitHub repo is already ready! Just make sure `stage4/` has:

- ✅ `Dockerfile` (already exists)
- ✅ `requirements.txt` (already exists)
- ✅ `docker-compose.production.yml` (already exists)

### Step 2: Sign Up for Render

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with your GitHub account (ahmedhaithamamer)
4. **No credit card required!**

### Step 3: Deploy API

1. Click **"New +"** → **"Web Service"**
2. Connect your repository: `ahmedhaithamamer/Depi_project_Data-science`
3. Configure:
   ```
   Name: walmart-forecast-api
   Region: Frankfurt (closest to you)
   Branch: main
   Root Directory: stage4
   Environment: Docker
   Instance Type: Free
   ```
4. Click **"Create Web Service"**

**Your API will be live at:**

```
https://walmart-forecast-api.onrender.com
```

### Step 4: Deploy Dashboard

1. Click **"New +"** → **"Web Service"**
2. Same repository: `ahmedhaithamamer/Depi_project_Data-science`
3. Configure:
   ```
   Name: walmart-forecast-dashboard
   Region: Frankfurt
   Branch: main
   Root Directory: stage4
   Environment: Docker
   Docker Command: streamlit run deployment/dashboard.py --server.port=$PORT
   Instance Type: Free
   ```
4. Click **"Create Web Service"**

**Your Dashboard will be live at:**

```
https://walmart-forecast-dashboard.onrender.com
```

### Step 5: Update Dashboard to Use API URL

Modify `stage4/deployment/dashboard.py` to use your Render API URL:

```python
# Change this line:
API_URL = "http://localhost:8000"

# To:
API_URL = "https://walmart-forecast-api.onrender.com"
```

Commit and push - Render will auto-deploy!

---

## 🎯 Alternative: Streamlit Cloud (Easiest!)

### Step 1: Create `streamlit_app.py` in Root

```python
import sys
from pathlib import Path

# Add stage4 to path
sys.path.insert(0, str(Path(__file__).parent / 'stage4'))

# Import and run dashboard
from deployment.dashboard import main

if __name__ == "__main__":
    main()
```

### Step 2: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click **"New app"**
4. Select:
   ```
   Repository: ahmedhaithamamer/Depi_project_Data-science
   Branch: main
   Main file: streamlit_app.py
   ```
5. Click **"Deploy"**

**Done! Your app will be at:**

```
https://ahmedhaithamamer-depi-project-data-science.streamlit.app
```

**Note:** This deploys dashboard only. For API, use PythonAnywhere (below).

---

## 🔧 Option: PythonAnywhere (Free API Hosting)

### For API Only

1. Sign up at https://www.pythonanywhere.com (100% free)
2. Go to **"Web"** tab → **"Add a new web app"**
3. Choose:
   ```
   Python version: 3.10
   Framework: Flask (we'll modify for FastAPI)
   ```
4. Upload your `stage4/` folder
5. Configure WSGI file to run FastAPI

**Your API will be at:**

```
https://yourusername.pythonanywhere.com
```

**Free Tier:**

- 512MB storage
- 100k API calls/day
- Enough for educational projects!

---

## 🎓 Hugging Face Spaces (For ML Demos)

Perfect for showcasing your ML model!

### Step 1: Create Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Choose:
   ```
   Space name: walmart-sales-forecasting
   License: MIT
   Space SDK: Streamlit
   ```

### Step 2: Upload Files

```bash
# Clone your space
git clone https://huggingface.co/spaces/yourusername/walmart-sales-forecasting

# Copy dashboard files
cp stage4/deployment/dashboard.py walmart-sales-forecasting/app.py
cp -r stage4/models walmart-sales-forecasting/
cp stage4/deployment/predictor.py walmart-sales-forecasting/

# Push to Hugging Face
cd walmart-sales-forecasting
git add .
git commit -m "Add Walmart forecasting app"
git push
```

**Your app will be live at:**

```
https://huggingface.co/spaces/yourusername/walmart-sales-forecasting
```

**Benefits:**

- ✅ Free GPU
- ✅ Great for portfolio
- ✅ Community visibility
- ✅ Easy sharing with professors/classmates

---

## 📊 Comparison: Free Platforms

| Platform            | API | Dashboard | Setup Time | Auto-Deploy | Portfolio Visibility |
| ------------------- | --- | --------- | ---------- | ----------- | -------------------- |
| **Render.com**      | ✅  | ✅        | 10 min     | ✅          | ⭐⭐⭐               |
| **Streamlit Cloud** | ❌  | ✅        | 5 min      | ✅          | ⭐⭐⭐⭐             |
| **Hugging Face**    | ❌  | ✅        | 10 min     | ✅          | ⭐⭐⭐⭐⭐           |
| **PythonAnywhere**  | ✅  | ❌        | 15 min     | ❌          | ⭐⭐                 |

---

## 🏆 Recommended Setup (100% Free)

### **For Educational Portfolio:**

```
┌─────────────────────────────┐
│   Hugging Face Spaces       │  ← Dashboard (Best for portfolio)
│   (Free + Community)        │
└─────────────┬───────────────┘
              │
              ↓
┌─────────────────────────────┐
│   PythonAnywhere            │  ← API (Free tier)
│   (Free API hosting)        │
└─────────────────────────────┘
```

**Why:**

- ✅ 100% FREE forever
- ✅ Great for showing to professors/recruiters
- ✅ Community engagement on Hugging Face
- ✅ Professional portfolio piece

### **For Quick Demo:**

```
┌─────────────────────────────┐
│   Streamlit Cloud           │  ← Everything in one!
│   (Free, 5 min setup)       │
└─────────────────────────────┘
```

**Why:**

- ✅ Fastest deployment (5 minutes)
- ✅ All-in-one solution
- ✅ Perfect for class presentations
- ✅ Easy to share link with classmates

---

## 🚀 Quickest Deployment (Right Now!)

### Deploy to Streamlit Cloud (5 Minutes)

1. **Create `streamlit_app.py` in root:**

```python
import sys
from pathlib import Path
import streamlit as st

# Add paths
sys.path.insert(0, str(Path(__file__).parent / 'stage4'))

# Run dashboard
from deployment.dashboard import *
```

2. **Push to GitHub:**

```bash
git add streamlit_app.py
git commit -m "Add Streamlit Cloud deployment"
git push
```

3. **Deploy:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repo
   - Done!

**🎉 You'll have a live demo in 5 minutes!**

---

## 💡 Tips for Free Tier

### Keep Services Awake

Free services sleep after inactivity. Use UptimeRobot (free) to ping every 5 minutes:

1. Sign up at https://uptimerobot.com (free)
2. Add monitor:
   ```
   Name: Walmart Forecast API
   URL: https://your-app.onrender.com/health
   Interval: 5 minutes
   ```

### Reduce Cold Start Time

In your `Dockerfile`, add:

```dockerfile
# Cache model loading
RUN python -c "import joblib; import pandas as pd; import numpy as np"
```

### Optimize for Low Memory

Free tiers have 512MB RAM. In `stage4/deployment/api.py`:

```python
# Load model lazily
@lru_cache(maxsize=1)
def get_model():
    return joblib.load("models/best_model.pkl")
```

---

## 🎓 Educational Benefits

### What to Include in Your Project Report

1. **Live Demo Links:**

   ```
   Dashboard: https://your-app.streamlit.app
   API: https://your-api.onrender.com
   Documentation: https://your-api.onrender.com/docs
   ```

2. **Deployment Architecture Diagram:**

   - Show free services used
   - Explain why you chose them
   - Cost-benefit analysis

3. **Screenshots:**
   - Dashboard in action
   - API documentation
   - Prediction results

### Impress Your Professors

- 🎯 Show live working demo (not just code!)
- 📊 Include deployment in presentation
- 🔗 Share link for testing
- 📈 Show logs/monitoring

---

## 🆘 Troubleshooting

### Service Sleeps After 15 Minutes

**Normal on free tier!** First request wakes it (~30 seconds).

**Solution:** Use UptimeRobot (free) to ping every 5 minutes.

### Out of Memory Error

**Reduce model size:**

```python
# In training, reduce model complexity
RandomForestRegressor(
    n_estimators=50,  # Instead of 100
    max_depth=10      # Instead of None
)
```

### Deployment Fails

**Check logs:**

- Render: Click on service → "Logs" tab
- Streamlit: Click "Manage app" → "Logs"

**Common fix:**

```bash
# Ensure requirements.txt has all dependencies
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## ✅ Next Steps

**Ready to deploy for free? Choose your path:**

### 🏃 **FASTEST (5 minutes):**

```bash
# Deploy to Streamlit Cloud
# See "Quickest Deployment" section above
```

### 🏆 **BEST FOR PORTFOLIO (10 minutes):**

```bash
# Deploy to Hugging Face Spaces
# See "Hugging Face Spaces" section above
```

### ⚖️ **MOST COMPLETE (15 minutes):**

```bash
# Deploy to Render.com (API + Dashboard)
# See "Quick Start: Render.com" section above
```

---

## 📞 Support

**Free Platform Docs:**

- Render: https://render.com/docs
- Streamlit Cloud: https://docs.streamlit.io/streamlit-community-cloud
- Hugging Face: https://huggingface.co/docs/hub/spaces
- PythonAnywhere: https://help.pythonanywhere.com/

**Community Help:**

- Streamlit Forum: https://discuss.streamlit.io/
- Hugging Face Discord: https://discord.gg/huggingface

---

**🎉 Ready to deploy for free? Let's start with Streamlit Cloud (5 minutes)!**
