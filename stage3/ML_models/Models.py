# Model training functions for Random Forest, XGBoost, and LightGBM.

from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import lightgbm as lgb
from Config import RANDOM_FOREST_PARAMS, XGBOOST_PARAMS, LIGHTGBM_PARAMS
from Evaluation import ModelEvaluator
import numpy as np

# Handles training of different ML models for sales forecasting.
class ModelTrainer:

    # Initialize model trainer with default configurations.
    def __init__(self):
        
        self.rf_params = RANDOM_FOREST_PARAMS
        self.xgb_params = XGBOOST_PARAMS
        self.lgb_params = LIGHTGBM_PARAMS
        self.evaluator = ModelEvaluator()
    
    # Train and evaluate Random Forest model-------------------------------------------------------
    def train_random_forest(self, X_train, y_train, X_test, y_test):

        print("Training Random Forest...")
        
        # Initialize and train the model
        model = RandomForestRegressor(**self.rf_params)
        model.fit(X_train, y_train)
        
        # Make predictions on test set
        y_pred = model.predict(X_test)
        
        # Evaluate performance
        metrics = self.evaluator.evaluate_predictions(y_test, y_pred)
        
        return model, y_pred, metrics

    # Train and evaluate XGBoost model-------------------------------------------------------------
    def train_xgboost(self, X_train, y_train, X_test, y_test):
        
        print("Training XGBoost...")
        
        # Initialize and train the model
        model = xgb.XGBRegressor(**self.xgb_params)
        
        # Train with evaluation set for monitoring
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            verbose=False
        )
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Evaluate
        metrics = self.evaluator.evaluate_predictions(y_test, y_pred)
        
        return model, y_pred, metrics

    # Train and evaluate LightGBM model------------------------------------------------------------
    def train_lightgbm(self, X_train, y_train, X_test, y_test):
        
        print("Training LightGBM...")
        
        # Initialize and train the model
        model = lgb.LGBMRegressor(**self.lgb_params)
        
        # Train with early stopping to prevent overfitting
        model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            callbacks=[
                lgb.early_stopping(50),  # Stop if no improvement for 50 rounds
                lgb.log_evaluation(0)     # Suppress output
            ]
        )
        
        # Make predictions
        y_pred = model.predict(X_test)
        
        # Evaluate
        metrics = self.evaluator.evaluate_predictions(y_test, y_pred)
        
        return model, y_pred, metrics
    
    # Create ensemble predictions by averaging ----------------------------------------------------
    # Combining different model strengths
    def create_ensemble_predictions(self, predictions_list):
     
        return np.mean(predictions_list, axis=0)