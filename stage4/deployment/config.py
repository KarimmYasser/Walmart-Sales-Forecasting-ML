"""
API Configuration Settings
"""

API_CONFIG = {
    # Server settings
    'host': '0.0.0.0',
    'port': 8000,
    'reload': True,
    'log_level': 'info',
    
    # CORS settings
    'cors_origins': [
        'http://localhost',
        'http://localhost:8000',
        'http://localhost:8501',  # Streamlit dashboard
        'http://127.0.0.1:8000',
        'http://127.0.0.1:8501',
    ],
    
    # Model settings
    'model_path': '../models/best_model.pkl',
    'model_reload_interval': 3600,  # seconds
    
    # Performance settings
    'max_batch_size': 1000,
    'cache_predictions': False,
    'cache_ttl': 300,  # seconds
    
    # Monitoring
    'enable_metrics': True,
    'log_predictions': True,
}

# Validation thresholds
VALIDATION_THRESHOLDS = {
    'min_temperature': -50,
    'max_temperature': 150,
    'min_fuel_price': 0,
    'max_fuel_price': 10,
    'min_cpi': 100,
    'max_cpi': 300,
    'min_unemployment': 0,
    'max_unemployment': 30,
    'min_size': 1000,
    'max_size': 250000,
}

# Default values for missing features
DEFAULT_VALUES = {
    'CPI': 211.0,
    'Unemployment': 7.5,
    'Temperature': 60.0,
    'Fuel_Price': 3.5,
}
