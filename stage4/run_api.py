"""
Helper script to run the FastAPI server with proper paths
Usage: python run_api.py
"""

import sys
import os
from pathlib import Path

# Add stage4 to Python path
stage4_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(stage4_dir))

# Change to stage4 directory
os.chdir(stage4_dir)

# Run uvicorn
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 Starting Walmart Sales Forecasting API")
    print("=" * 70)
    print(f"📁 Working directory: {stage4_dir}")
    print("=" * 70)
    print("\n🌐 API will be available at:")
    print("   - Swagger UI: http://localhost:8000/docs")
    print("   - ReDoc: http://localhost:8000/redoc")
    print("   - Health: http://localhost:8000/health")
    print("⏹️  Press Ctrl+C to stop\n")
    
    uvicorn.run(
        "deployment.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
