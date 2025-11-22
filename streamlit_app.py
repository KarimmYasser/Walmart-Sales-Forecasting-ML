"""
Streamlit Cloud Entry Point for Walmart Sales Forecasting Dashboard

This file serves as the main entry point when deploying to Streamlit Cloud.
It sets up the necessary paths and imports the dashboard from stage4.
"""

import sys
from pathlib import Path

# Add stage4 to Python path
stage4_path = Path(__file__).parent / 'stage4'
sys.path.insert(0, str(stage4_path))

# Add stage3 ML_models to path
stage3_path = Path(__file__).parent / 'stage3' / 'ML_models'
sys.path.insert(0, str(stage3_path))

# Import and run the dashboard
# Import after path setup (lint warning is expected - paths are set dynamically at runtime)
from dashboard.app import *  # type: ignore

# The dashboard will run automatically when this script is executed
# Streamlit Cloud will detect and run this file
