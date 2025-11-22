"""
Helper script to run the Streamlit dashboard with proper paths
Usage: python run_dashboard.py
"""

import sys
import os
from pathlib import Path

# Add stage4 to Python path
stage4_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(stage4_dir))

# Change to stage4 directory
os.chdir(stage4_dir)

# Run streamlit
if __name__ == "__main__":
    import subprocess
    
    dashboard_path = stage4_dir / "dashboard" / "app.py"
    
    print("=" * 70)
    print("🚀 Starting Walmart Sales Forecasting Dashboard")
    print("=" * 70)
    print(f"📁 Working directory: {stage4_dir}")
    print(f"📊 Dashboard: {dashboard_path}")
    print("=" * 70)
    print("\n🌐 Dashboard will open at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop\n")
    
    subprocess.run([
        sys.executable, 
        "-m", 
        "streamlit", 
        "run", 
        str(dashboard_path),
        "--server.port", "8501",
        "--server.address", "localhost"
    ])
