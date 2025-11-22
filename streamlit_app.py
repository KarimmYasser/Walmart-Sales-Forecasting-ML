"""
Streamlit Cloud Entry Point for Walmart Sales Forecasting Dashboard

This file serves as the main entry point when deploying to Streamlit Cloud.
It sets up the necessary paths and imports the dashboard from stage4.
"""

import sys
import streamlit as st
from pathlib import Path

# Add stage4 to Python path
stage4_path = Path(__file__).parent / 'stage4'
sys.path.insert(0, str(stage4_path))

# Add stage3 ML_models to path
stage3_path = Path(__file__).parent / 'stage3' / 'ML_models'
sys.path.insert(0, str(stage3_path))

# Import and run the dashboard with error handling
try:
    from dashboard.app import *  # type: ignore
except ImportError as e:
    st.error(f"❌ Failed to import dashboard: {e}")
    st.info("📝 Debug Info:")
    st.write(f"- Current file: {__file__}")
    st.write(f"- stage4_path: {stage4_path}")
    st.write(f"- stage4 exists: {stage4_path.exists()}")
    st.write(f"- sys.path: {sys.path[:3]}")
    st.stop()
except Exception as e:
    st.error(f"❌ Unexpected error: {e}")
    st.exception(e)
    st.stop()
