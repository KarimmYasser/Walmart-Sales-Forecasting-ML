# Main SalesForecaster class that orchestrates the entire ML pipeline.
import pandas as pd
import numpy as np
from Config import MODELING_STAGES, STORE_TYPES, TRAIN_TEST_SPLIT_RATIO
from Feature_Engineering import FeatureSelector
from Models import ModelTrainer
from Evaluation import ModelEvaluator

#    Main class for sales forecasting with progressive modeling and ensembling.
    
    # This class orchestrates:
    # - Progressive feature selection
    # - Multiple model training
    # - Model evaluation and comparison
    # - Store-type-specific modeling
    # - Ensemble predictions

class SalesForecaster:

    # Initialize the forecaster with necessary components.
    def __init__(self):
        
        self.feature_selector = FeatureSelector()
        self.model_trainer = ModelTrainer()
        self.evaluator = ModelEvaluator()
        self.results = {}
    
    # Implement progressive modeling strategy with increasing feature complexity.
    # At each stage, train all three models and compare performance.
    def progressive_modeling(self, df, target_col='Weekly_Sales'):
     
        all_results = {}
        
        # Sort by date to ensure proper time series split
        df_sorted = df.sort_values('Date').reset_index(drop=True)
        y = df_sorted[target_col]
        
        # Iterate through progressive modeling stages
        for stage in MODELING_STAGES:
            print(f"\n{'='*60}")
            print(f"Stage: {stage.upper()}")
            print(f"{'='*60}")
            
            # Get features for current stage
            features = self.feature_selector.get_features_by_stage(stage)
            X = df_sorted[features]
            
            # Time series split 80 training, 20 testing
            split_idx = int(len(X) * TRAIN_TEST_SPLIT_RATIO)
            X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            print(f"Features: {len(features)}")
            print(f"Train samples: {len(X_train)}, Test samples: {len(X_test)}")
            
            stage_results = {}
            predictions_list = []
            
            # Train Random Forest -----------------------------------------------------------------
            rf_model, rf_pred, rf_metrics = self.model_trainer.train_random_forest(
                X_train, y_train, X_test, y_test
            )
            stage_results['random_forest'] = {
                'model': rf_model,
                'predictions': rf_pred,
                'metrics': rf_metrics
            }
            predictions_list.append(rf_pred)
            
            # Train XGBoost -----------------------------------------------------------------------
            xgb_model, xgb_pred, xgb_metrics = self.model_trainer.train_xgboost(
                X_train, y_train, X_test, y_test
            )
            stage_results['xgboost'] = {
                'model': xgb_model,
                'predictions': xgb_pred,
                'metrics': xgb_metrics
            }
            predictions_list.append(xgb_pred)
            
            # Train LightGBM ----------------------------------------------------------------------
            lgb_model, lgb_pred, lgb_metrics = self.model_trainer.train_lightgbm(
                X_train, y_train, X_test, y_test
            )
            stage_results['lightgbm'] = {
                'model': lgb_model,
                'predictions': lgb_pred,
                'metrics': lgb_metrics
            }
            predictions_list.append(lgb_pred)
            
            # Create ensemble predictions (simple average)
            ensemble_pred = self.model_trainer.create_ensemble_predictions(predictions_list)
            ensemble_metrics = self.evaluator.evaluate_predictions(y_test, ensemble_pred)
            stage_results['ensemble'] = {
                'predictions': ensemble_pred,
                'metrics': ensemble_metrics
            }
            
            # Print results for this stage
            print(f"\n{stage.upper()} Results:")
            self.evaluator.print_metrics(rf_metrics, "Random Forest")
            self.evaluator.print_metrics(xgb_metrics, "XGBoost")
            self.evaluator.print_metrics(lgb_metrics, "LightGBM")
            self.evaluator.print_metrics(ensemble_metrics, "Ensemble")
            
            all_results[stage] = stage_results
        
        self.results = all_results
        return all_results
    
    # Train separate models for each store type (A, B, C).

        # Store-type-specific models can capture unique patterns for each type:
        # - Type A stores might have different seasonality
        # - Type B stores might respond differently to promotions
        # - Type C stores might have different customer behavior

    def train_store_type_models(self, df, target_col='Weekly_Sales'):

        print(f"\n{'='*60}")
        print("STORE-TYPE-SPECIFIC MODELING")
        print(f"{'='*60}")
        
        store_type_results = {}
        features = self.feature_selector.get_features_by_stage('full')
        
        for store_type in STORE_TYPES:
            print(f"\n{store_type}:")
            
            # Filter data for this store type
            df_type = df[df[store_type] == True].copy()
            
            if len(df_type) < 100:  # Skip if insufficient data
                print(f"Insufficient data ({len(df_type)} samples), skipping...")
                continue
            
            # Sort by date
            df_type = df_type.sort_values('Date').reset_index(drop=True)
            
            X = df_type[features]
            y = df_type[target_col]
            
            # Split data
            split_idx = int(len(X) * TRAIN_TEST_SPLIT_RATIO)
            X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
            y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
            
            # Train all three models
            rf_model, rf_pred, _ = self.model_trainer.train_random_forest(
                X_train, y_train, X_test, y_test
            )
            xgb_model, xgb_pred, _ = self.model_trainer.train_xgboost(
                X_train, y_train, X_test, y_test
            )
            lgb_model, lgb_pred, _ = self.model_trainer.train_lightgbm(
                X_train, y_train, X_test, y_test
            )
            
            # Create ensemble
            ensemble_pred = self.model_trainer.create_ensemble_predictions(
                [rf_pred, xgb_pred, lgb_pred]
            )
            metrics = self.evaluator.evaluate_predictions(y_test, ensemble_pred)
            
            print(f"Samples: {len(df_type)}, Test MAE: {metrics['MAE']:.2f}, "
                  f"R2: {metrics['R2']:.4f}")
            
            store_type_results[store_type] = {
                'models': {
                    'random_forest': rf_model,
                    'xgboost': xgb_model,
                    'lightgbm': lgb_model
                },
                'metrics': metrics,
                'predictions': ensemble_pred
            }
        
        return store_type_results
    
    # Extract and display feature importance from trained models.
        
        #Feature importance helps you understand:
        #- Which features drive predictions most
        #- Which data to prioritize collecting
        #- Which features might be redundant
    def get_feature_importance(self, model_name='random_forest', stage='full'):

        if not self.results:
            print("No results available. Train models first.")
            return None
        
        model = self.results[stage][model_name]['model']
        features = self.feature_selector.get_features_by_stage(stage)
        
        # Get feature importance
        if hasattr(model, 'feature_importances_'):
            importance = model.feature_importances_
        else:
            print("Model doesn't support feature importance.")
            return None
        
        # Create DataFrame
        importance_df = pd.DataFrame({
            'Feature': features,
            'Importance': importance
        }).sort_values('Importance', ascending=False)
        
        return importance_df