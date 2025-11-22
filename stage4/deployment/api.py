"""
FastAPI REST API for Sales Forecasting
Serves predictions via HTTP endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uvicorn
from deployment.predictor import SalesPredictor
from deployment.config import API_CONFIG

# Initialize FastAPI app
app = FastAPI(
    title="Walmart Sales Forecasting API",
    description="REST API for predicting weekly sales using machine learning",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=API_CONFIG['cors_origins'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize predictor (loads model once at startup)
predictor = SalesPredictor()


# Request/Response Models
class PredictionRequest(BaseModel):
    """Single prediction request."""
    Store: int = Field(..., ge=1, le=45, description="Store number (1-45)")
    Dept: int = Field(..., ge=1, le=99, description="Department number (1-99)")
    Date: str = Field(..., description="Date in YYYY-MM-DD format")
    IsHoliday: bool = Field(False, description="Is it a holiday week?")
    Temperature: float = Field(..., description="Temperature in Fahrenheit")
    Fuel_Price: float = Field(..., description="Fuel price in dollars")
    CPI: Optional[float] = Field(None, description="Consumer Price Index")
    Unemployment: Optional[float] = Field(None, description="Unemployment rate")
    Type: str = Field(..., description="Store type (A, B, or C)")
    Size: int = Field(..., description="Store size in square feet")
    
    class Config:
        schema_extra = {
            "example": {
                "Store": 1,
                "Dept": 1,
                "Date": "2023-11-24",
                "IsHoliday": True,
                "Temperature": 42.31,
                "Fuel_Price": 2.572,
                "CPI": 211.096,
                "Unemployment": 8.106,
                "Type": "A",
                "Size": 151315
            }
        }


class BatchPredictionRequest(BaseModel):
    """Batch prediction request."""
    predictions: List[PredictionRequest]


class PredictionResponse(BaseModel):
    """Prediction response."""
    Store: int
    Dept: int
    Date: str
    predicted_sales: float
    confidence_interval_lower: Optional[float] = None
    confidence_interval_upper: Optional[float] = None
    prediction_timestamp: str


class BatchPredictionResponse(BaseModel):
    """Batch prediction response."""
    predictions: List[PredictionResponse]
    total_predicted_sales: float
    count: int


class ModelInfo(BaseModel):
    """Model information response."""
    model_type: str
    model_version: str
    features_count: int
    performance_metrics: dict
    last_trained: str
    status: str


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    api_version: str
    timestamp: str


# API Endpoints

@app.get("/", tags=["General"])
async def root():
    """Root endpoint."""
    return {
        "message": "Walmart Sales Forecasting API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthCheck, tags=["General"])
async def health_check():
    """Check API and model health."""
    return {
        "status": "healthy" if predictor.model is not None else "unhealthy",
        "model_loaded": predictor.model is not None,
        "api_version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/model/info", response_model=ModelInfo, tags=["Model"])
async def get_model_info():
    """Get information about the loaded model."""
    if predictor.model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return predictor.get_model_info()


@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_single(request: PredictionRequest):
    """
    Make a single sales prediction.
    
    Returns predicted weekly sales for given store, department, and date.
    """
    try:
        # Convert request to dict
        input_data = request.dict()
        
        # Make prediction
        prediction = predictor.predict_single(input_data)
        
        return {
            "Store": request.Store,
            "Dept": request.Dept,
            "Date": request.Date,
            "predicted_sales": round(prediction['predicted_sales'], 2),
            "confidence_interval_lower": round(prediction.get('ci_lower', 0), 2),
            "confidence_interval_upper": round(prediction.get('ci_upper', 0), 2),
            "prediction_timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Make batch predictions for multiple records.
    
    Useful for forecasting multiple stores/departments at once.
    """
    try:
        # Convert requests to list of dicts
        input_data = [req.dict() for req in request.predictions]
        
        # Make batch prediction
        predictions = predictor.predict_batch(input_data)
        
        # Format response
        prediction_responses = []
        total_sales = 0
        
        for pred in predictions:
            prediction_responses.append({
                "Store": pred['Store'],
                "Dept": pred['Dept'],
                "Date": pred['Date'],
                "predicted_sales": round(pred['predicted_sales'], 2),
                "confidence_interval_lower": round(pred.get('ci_lower', 0), 2),
                "confidence_interval_upper": round(pred.get('ci_upper', 0), 2),
                "prediction_timestamp": datetime.now().isoformat()
            })
            total_sales += pred['predicted_sales']
        
        return {
            "predictions": prediction_responses,
            "total_predicted_sales": round(total_sales, 2),
            "count": len(prediction_responses)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/predict/store/{store_id}", tags=["Predictions"])
async def predict_store(
    store_id: int,
    date: str,
    top_departments: int = 10
):
    """
    Predict sales for top departments in a specific store.
    
    Parameters:
    - store_id: Store number (1-45)
    - date: Date in YYYY-MM-DD format
    - top_departments: Number of top departments to predict (default: 10)
    """
    try:
        predictions = predictor.predict_store_forecast(store_id, date, top_departments)
        return {
            "store_id": store_id,
            "date": date,
            "predictions": predictions,
            "total_predicted_sales": sum(p['predicted_sales'] for p in predictions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/predict/week", tags=["Predictions"])
async def predict_week(
    store_id: int,
    dept_id: int,
    start_date: str,
    weeks: int = 4
):
    """
    Predict sales for multiple weeks ahead.
    
    Parameters:
    - store_id: Store number
    - dept_id: Department number
    - start_date: Starting date (YYYY-MM-DD)
    - weeks: Number of weeks to forecast (default: 4)
    """
    try:
        predictions = predictor.predict_multi_week(store_id, dept_id, start_date, weeks)
        return {
            "store_id": store_id,
            "dept_id": dept_id,
            "predictions": predictions,
            "total_predicted_sales": sum(p['predicted_sales'] for p in predictions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/stats/performance", tags=["Statistics"])
async def get_performance_stats():
    """Get model performance statistics."""
    return predictor.get_performance_metrics()


@app.post("/reload", tags=["Model"])
async def reload_model():
    """Reload the model from disk."""
    try:
        predictor.load_model()
        return {
            "status": "success",
            "message": "Model reloaded successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run the API server
    uvicorn.run(
        "api:app",
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        reload=API_CONFIG['reload'],
        log_level=API_CONFIG['log_level']
    )
