"""
Vercel Serverless Function Entry Point
This wraps the FastAPI app for Vercel deployment
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / 'stage4'))
sys.path.insert(0, str(project_root / 'stage3' / 'ML_models'))

# Import the FastAPI app
from stage4.deployment.api import app

# Vercel handler
def handler(event, context):
    """Vercel serverless function handler"""
    return app
