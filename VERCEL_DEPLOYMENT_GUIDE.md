# 🚀 Vercel Deployment Guide

Complete guide for deploying the Walmart Sales Forecasting API to Vercel.

> **⚠️ Important Limitations**:
>
> - Vercel is optimized for serverless functions and has a **50MB limit** per function
> - The trained model file (best_model.pkl) is ~200MB, which **exceeds Vercel's limit**
> - **Recommended Alternative**: Deploy to a cloud VM (Azure, AWS, GCP) for full functionality
> - This guide shows how to deploy the API only; Dashboard requires a separate solution

---

## 📋 What Works on Vercel

✅ **API Endpoints** (without model loading)  
✅ **Feature Engineering**  
✅ **Mock Predictions** (for demonstration)  
❌ **Full Model** (exceeds 50MB limit)  
❌ **Streamlit Dashboard** (not supported)

---

## 🎯 Deployment Options

### Option 1: API-Only Deployment (Mock Predictions)

Deploy a lightweight API that demonstrates the interface without the full model.

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Login to Vercel

```bash
vercel login
```

#### Step 3: Deploy

```bash
# Navigate to project root
cd d:\Projects\DEPI\Depi_project_Data-science

# Deploy to Vercel
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? Your account
# - Link to existing project? No
# - Project name? walmart-sales-forecasting
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

#### Step 4: Access Your API

After deployment, Vercel will provide a URL like:

```
https://walmart-sales-forecasting.vercel.app
```

Test endpoints:

- Health: `https://your-app.vercel.app/health`
- API Docs: `https://your-app.vercel.app/docs`
- Predict: `https://your-app.vercel.app/predict` (POST)

---

### Option 2: Hybrid Deployment (Recommended)

Deploy API on Vercel with model hosted externally.

#### Architecture:

```
┌─────────────────┐
│  Vercel (API)   │ ──→ Lightweight endpoints
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Cloud Storage  │ ──→ Model file (Azure Blob/AWS S3)
│  (Model Host)   │
└─────────────────┘
```

#### Step 1: Upload Model to Cloud Storage

**Azure Blob Storage:**

```bash
# Install Azure CLI
az storage blob upload \
  --account-name youraccount \
  --container-name models \
  --name best_model.pkl \
  --file stage4/models/best_model.pkl
```

**AWS S3:**

```bash
aws s3 cp stage4/models/best_model.pkl \
  s3://your-bucket/models/best_model.pkl
```

#### Step 2: Update Predictor to Load from URL

Modify `stage4/deployment/predictor.py`:

```python
import requests

def load_model_from_url(url):
    response = requests.get(url)
    model = joblib.loads(response.content)
    return model

# In __init__:
MODEL_URL = "https://your-storage-url/best_model.pkl"
self.model = load_model_from_url(MODEL_URL)
```

#### Step 3: Deploy to Vercel

```bash
vercel --prod
```

---

### Option 3: Full Solution on Different Platform

Since Vercel has limitations, here are better alternatives:

#### **Recommended: Railway.app** (Similar to Vercel, but supports Docker)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
cd stage4
railway up
```

**Advantages:**

- Supports Docker containers (no size limits)
- Can run both API and Dashboard
- Similar pricing to Vercel
- Easy deployment

#### **Alternative: Render.com** (Free tier available)

1. Go to https://render.com
2. Connect GitHub repository
3. Select "Web Service"
4. Docker configuration:
   ```yaml
   - Name: walmart-forecast-api
   - Environment: Docker
   - Docker Command: uvicorn deployment.api:app --host 0.0.0.0 --port $PORT
   ```

---

## 🔧 Vercel Configuration Files

### vercel.json

```json
{
  "version": 2,
  "name": "walmart-sales-forecasting",
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/index.py"
    }
  ]
}
```

### requirements-vercel.txt

```txt
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.5.0
scikit-learn==1.3.2
pandas==2.1.3
numpy==1.24.3
joblib==1.3.2
python-multipart==0.0.6
```

---

## 📊 Comparison: Vercel vs Alternatives

| Feature               | Vercel     | Railway     | Render      | Cloud VM      |
| --------------------- | ---------- | ----------- | ----------- | ------------- |
| **Model Size Limit**  | 50MB ❌    | No limit ✅ | No limit ✅ | No limit ✅   |
| **Dashboard Support** | No ❌      | Yes ✅      | Yes ✅      | Yes ✅        |
| **Docker Support**    | No ❌      | Yes ✅      | Yes ✅      | Yes ✅        |
| **Free Tier**         | Yes ✅     | $5/month    | Yes ✅      | From $5/month |
| **Ease of Use**       | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐    | ⭐⭐⭐⭐    | ⭐⭐⭐        |
| **Setup Time**        | 5 min      | 10 min      | 10 min      | 15 min        |

---

## 🎯 Recommended Deployment Path

Given your requirements (API + Dashboard on same server), here's the best approach:

### **Best Option: Railway.app**

**Why:**

- ✅ Supports Docker (no size limits)
- ✅ Can deploy both API and Dashboard
- ✅ Single domain with routing
- ✅ Easy GitHub integration
- ✅ Affordable ($5-10/month)

**Steps:**

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize project
cd d:\Projects\DEPI\Depi_project_Data-science\stage4
railway init

# 4. Deploy
railway up

# 5. Configure services
railway service add api
railway service add dashboard

# 6. Set up domains
railway domain
```

**Access:**

- Dashboard: `https://your-app.up.railway.app/`
- API: `https://your-app.up.railway.app/api/`

---

## 🚨 Troubleshooting Vercel

### Error: Function size exceeds limit

**Solution 1**: Use external model hosting (Option 2 above)

**Solution 2**: Switch to Railway/Render (supports larger deployments)

### Error: Module not found

```bash
# Ensure requirements-vercel.txt is in root
# Rebuild
vercel --prod --force
```

### Cold Start Issues

Vercel serverless functions "sleep" after inactivity:

- First request may take 10-30 seconds
- Subsequent requests are faster
- Consider keeping warm with a cron job

---

## 💡 Quick Migration to Railway

If Vercel doesn't work due to size limits:

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and initialize
railway login
cd stage4
railway init

# 3. Deploy using Docker Compose
railway up --file docker-compose.production.yml

# 4. Done! Get URL
railway domain
```

**Result**: Full working deployment with API + Dashboard in under 10 minutes! 🎉

---

## 📞 Support

**Vercel Issues:**

- Vercel Docs: https://vercel.com/docs
- Community: https://github.com/vercel/vercel/discussions

**Alternative Platforms:**

- Railway: https://railway.app/
- Render: https://render.com/
- Cloud VM Guide: See `CLOUD_DEPLOYMENT_GUIDE.md`

---

## ✅ Recommendation

**For this project, I recommend:**

1. **Best Choice**: Deploy to **Railway.app** or **Render.com**

   - Supports full Docker setup
   - Both API and Dashboard
   - Single domain
   - Easy to use

2. **Second Choice**: Deploy to **Cloud VM** (Azure/AWS/GCP)

   - Most control
   - Best performance
   - See `CLOUD_DEPLOYMENT_GUIDE.md`

3. **Vercel**: Only suitable if you:
   - Host model externally
   - Only need API (not Dashboard)
   - Accept cold start delays

---

**🎉 Ready to deploy? Run:**

```bash
# For Railway (Recommended)
npm install -g @railway/cli
railway login
cd stage4
railway up

# For Cloud VM (Best Performance)
# See CLOUD_DEPLOYMENT_GUIDE.md
```
