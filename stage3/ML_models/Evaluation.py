# Model evaluation utilities including metrics calculation and cross-validation.

import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from Config import CV_SPLITS

# Handles model evaluation and cross-validation for time series data.
class ModelEvaluator:
    
    @staticmethod
    def evaluate_predictions(y_true, y_pred):
       
        
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        r2 = r2_score(y_true, y_pred)
        
        return {
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2
        }
    
    
    @staticmethod
    def print_metrics(metrics, model_name="Model"):

        print(f"{model_name:15s} - MAE: {metrics['MAE']:8.2f}, "
              f"RMSE: {metrics['RMSE']:8.2f}, "
              f"R2: {metrics['R2']:7.4f}")
