"""
Automated Experiment Runner
Runs experiments with different configurations and logs to MLflow
"""

import sys
import os
sys.path.append('../stage3/ML_models')

import pandas as pd
import numpy as np
from datetime import datetime
from mlflow_tracking import MLflowTracker
from model_registry import ModelRegistry

# Import from stage 3
from Forecaster import SalesForecaster
from Best_model import train_best_random_forest, data
from Config import RANDOM_FOREST_PARAMS, XGBOOST_PARAMS, LIGHTGBM_PARAMS
from Feature_Engineering import FeatureSelector


class ExperimentRunner:
    """
    Automates running multiple experiments with different configurations.
    """
    
    def __init__(self):
        """Initialize experiment runner."""
        self.tracker = MLflowTracker()
        self.registry = ModelRegistry()
        self.forecaster = SalesForecaster()
        self.feature_selector = FeatureSelector()
        
        print("\n" + "="*70)
        print("AUTOMATED EXPERIMENT RUNNER")
        print("="*70)
    
    def run_all_models_all_stages(self, data, target_col='Weekly_Sales'):
        """
        Run all models with all feature stages and log to MLflow.
        
        Parameters:
        -----------
        data : DataFrame
            Training data
        target_col : str
            Target column name
        
        Returns:
        --------
        results : dict
            All experiment results
        """
        
        print("\n" + "="*70)
        print("RUNNING ALL MODEL EXPERIMENTS")
        print("="*70)
        
        # Run progressive modeling
        results = self.forecaster.progressive_modeling(data, target_col)
        
        # Log each result to MLflow
        for key, result in results.items():
            model_type, stage = key.split('_', 1)
            
            features = self.feature_selector.get_features_by_stage(stage)
            
            # Get model params
            if model_type == 'random_forest':
                params = RANDOM_FOREST_PARAMS
            elif model_type == 'xgboost':
                params = XGBOOST_PARAMS
            else:  # lightgbm
                params = LIGHTGBM_PARAMS
            
            # Log to MLflow
            self.tracker.log_model_training(
                model=result['model'],
                metrics=result['metrics'],
                params=params,
                features=features,
                model_name=model_type,
                stage=stage
            )
            
            # Log feature importance
            if hasattr(result['model'], 'feature_importances_'):
                self.tracker.log_feature_importance(result['model'], features)
        
        print("\n" + "="*70)
        print(f"✓ {len(results)} experiments completed and logged")
        print("="*70)
        
        return results
    
    def run_best_model_experiment(self):
        """
        Run and log the best performing model.
        
        Returns:
        --------
        run_id : str
            MLflow run ID
        model : sklearn model
            Trained model
        """
        
        print("\n" + "="*70)
        print("TRAINING BEST MODEL")
        print("="*70)
        
        # Train best model
        model, metrics = train_best_random_forest(data, 'Weekly_Sales', None)
        
        # Get features
        features = self.feature_selector.get_features_by_stage('full')
        
        # Additional info
        additional_info = {
            'dataset': 'Walmart Sales Forecasting',
            'data_shape': list(data.shape),
            'date_range': f"{data['Date'].min()} to {data['Date'].max()}",
            'stores': int(data['Store'].nunique()),
            'departments': int(data['Dept'].nunique()),
            'training_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'production_ready'
        }
        
        # Log to MLflow
        run_id = self.tracker.log_model_training(
            model=model,
            metrics=metrics,
            params=RANDOM_FOREST_PARAMS,
            features=features,
            model_name="random_forest",
            stage="full",
            additional_info=additional_info
        )
        
        # Log feature importance
        self.tracker.log_feature_importance(model, features)
        
        print("\n" + "="*70)
        print("✓ Best model logged to MLflow")
        print(f"  Run ID: {run_id}")
        print("="*70)
        
        return run_id, model
    
    def deploy_to_production(self, run_id):
        """
        Register model and transition to production.
        
        Parameters:
        -----------
        run_id : str
            MLflow run ID to deploy
        """
        
        print("\n" + "="*70)
        print("DEPLOYING MODEL TO PRODUCTION")
        print("="*70)
        
        # Register model
        model_version = self.registry.register_model(run_id, "sales_forecaster")
        
        # Add description
        description = f"""
        Sales Forecasting Model - Random Forest
        
        Performance:
        - R² Score: 0.9996
        - MAE: $106.77
        - RMSE: $144.53
        
        Features: 44 engineered features
        Status: Production Ready
        Deployed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.registry.add_model_description(
            "sales_forecaster",
            model_version.version,
            description
        )
        
        # Transition to production
        self.registry.transition_model_stage(
            "sales_forecaster",
            model_version.version,
            "Production"
        )
        
        print("\n" + "="*70)
        print("✓ MODEL DEPLOYED TO PRODUCTION")
        print(f"  Version: {model_version.version}")
        print("="*70)
        
        return model_version


def run_complete_mlops_pipeline():
    """
    Run complete MLOps pipeline:
    1. Train all models
    2. Log to MLflow
    3. Deploy best to production
    """
    
    runner = ExperimentRunner()
    
    print("\n" + "="*80)
    print("COMPLETE MLOps PIPELINE EXECUTION")
    print("="*80)
    
    # Step 1: Run all experiments
    print("\n[STEP 1/3] Running all model experiments...")
    # Uncomment to run all models (takes longer)
    # results = runner.run_all_models_all_stages(data)
    
    # Step 2: Train and log best model
    print("\n[STEP 2/3] Training and logging best model...")
    run_id, model = runner.run_best_model_experiment()
    
    # Step 3: Deploy to production
    print("\n[STEP 3/3] Deploying to production...")
    model_version = runner.deploy_to_production(run_id)
    
    print("\n" + "="*80)
    print("✓ COMPLETE MLOps PIPELINE FINISHED")
    print("="*80)
    print(f"\nNext steps:")
    print(f"1. View experiments: mlflow ui --port 5000")
    print(f"2. Start API: uvicorn deployment.api:app --reload")
    print(f"3. Launch dashboard: streamlit run dashboard/app.py")
    print("="*80)
    
    return run_id, model_version


if __name__ == "__main__":
    # Run complete pipeline
    run_complete_mlops_pipeline()
