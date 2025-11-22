"""
MLflow Tracking and Experiment Management
Logs models, parameters, metrics, and artifacts to MLflow
"""

import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from pathlib import Path


class MLflowTracker:
    """
    Handles MLflow experiment tracking for sales forecasting models.
    """
    
    def __init__(self, experiment_name="walmart_sales_forecasting", tracking_uri="./mlruns"):
        """
        Initialize MLflow tracker.
        
        Parameters:
        -----------
        experiment_name : str
            Name of the MLflow experiment
        tracking_uri : str
            URI for MLflow tracking server
        """
        self.experiment_name = experiment_name
        mlflow.set_tracking_uri(tracking_uri)
        
        # Create or get experiment
        try:
            experiment_id = mlflow.create_experiment(experiment_name)
        except:
            experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        
        self.experiment_id = experiment_id
        mlflow.set_experiment(experiment_name)
        
        print(f"✓ MLflow tracking initialized")
        print(f"  Experiment: {experiment_name}")
        print(f"  Tracking URI: {tracking_uri}")
    
    def log_model_training(self, model, metrics, params, features, 
                          model_name="random_forest", stage="full",
                          additional_info=None):
        """
        Log a complete model training run to MLflow.
        
        Parameters:
        -----------
        model : sklearn model
            Trained model object
        metrics : dict
            Performance metrics (MAE, RMSE, R2)
        params : dict
            Model hyperparameters
        features : list
            List of feature names used
        model_name : str
            Name/type of model
        stage : str
            Feature stage used
        additional_info : dict
            Any additional information to log
        """
        
        with mlflow.start_run(run_name=f"{model_name}_{stage}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
            
            # Log parameters
            mlflow.log_param("model_type", model_name)
            mlflow.log_param("feature_stage", stage)
            mlflow.log_param("num_features", len(features))
            
            # Log model hyperparameters
            for param_name, param_value in params.items():
                mlflow.log_param(param_name, param_value)
            
            # Log metrics
            mlflow.log_metric("mae", metrics['MAE'])
            mlflow.log_metric("rmse", metrics['RMSE'])
            mlflow.log_metric("r2_score", metrics['R2'])
            mlflow.log_metric("accuracy_percent", metrics['R2'] * 100)
            
            # Log model
            mlflow.sklearn.log_model(
                model, 
                "model",
                registered_model_name=f"sales_forecaster_{model_name}"
            )
            
            # Log features as artifact
            features_df = pd.DataFrame({'feature': features})
            features_path = "features.csv"
            features_df.to_csv(features_path, index=False)
            mlflow.log_artifact(features_path)
            os.remove(features_path)
            
            # Log additional info
            if additional_info:
                info_path = "additional_info.json"
                with open(info_path, 'w') as f:
                    json.dump(additional_info, f, indent=2)
                mlflow.log_artifact(info_path)
                os.remove(info_path)
            
            # Set tags
            mlflow.set_tag("stage", "production" if metrics['R2'] > 0.95 else "experimental")
            mlflow.set_tag("deployment_ready", str(metrics['R2'] > 0.90))
            mlflow.set_tag("date", datetime.now().strftime('%Y-%m-%d'))
            
            run_id = mlflow.active_run().info.run_id
            
            print(f"\n✓ Model logged to MLflow")
            print(f"  Run ID: {run_id}")
            print(f"  Model: {model_name}")
            print(f"  R² Score: {metrics['R2']:.4f}")
            
            return run_id
    
    def log_feature_importance(self, model, feature_names, top_n=20):
        """
        Log feature importance as an artifact.
        
        Parameters:
        -----------
        model : sklearn model
            Trained model with feature_importances_
        feature_names : list
            Names of features
        top_n : int
            Number of top features to display
        """
        
        if hasattr(model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            # Log top features as metrics
            for idx, row in importance_df.head(top_n).iterrows():
                mlflow.log_metric(f"importance_{row['feature']}", row['importance'])
            
            # Save full importance as artifact
            importance_path = "feature_importance.csv"
            importance_df.to_csv(importance_path, index=False)
            mlflow.log_artifact(importance_path)
            os.remove(importance_path)
            
            print(f"✓ Feature importance logged ({len(feature_names)} features)")
    
    def load_model_by_run_id(self, run_id):
        """
        Load a model from MLflow by run ID.
        
        Parameters:
        -----------
        run_id : str
            MLflow run ID
        
        Returns:
        --------
        model : sklearn model
            Loaded model
        """
        
        model_uri = f"runs:/{run_id}/model"
        model = mlflow.sklearn.load_model(model_uri)
        print(f"✓ Model loaded from run: {run_id}")
        return model
    
    def get_best_model(self, metric="r2_score", ascending=False):
        """
        Retrieve the best model based on a metric.
        
        Parameters:
        -----------
        metric : str
            Metric to optimize
        ascending : bool
            Sort order
        
        Returns:
        --------
        run_id : str
            Run ID of best model
        model : sklearn model
            Best model
        """
        
        # Search for runs
        runs = mlflow.search_runs(
            experiment_ids=[self.experiment_id],
            order_by=[f"metrics.{metric} {'ASC' if ascending else 'DESC'}"]
        )
        
        if len(runs) == 0:
            print("No runs found")
            return None, None
        
        best_run = runs.iloc[0]
        run_id = best_run['run_id']
        
        # Load model
        model = self.load_model_by_run_id(run_id)
        
        print(f"\n✓ Best model retrieved")
        print(f"  Run ID: {run_id}")
        print(f"  {metric}: {best_run[f'metrics.{metric}']:.4f}")
        
        return run_id, model
    
    def compare_runs(self, run_ids):
        """
        Compare multiple runs.
        
        Parameters:
        -----------
        run_ids : list
            List of run IDs to compare
        
        Returns:
        --------
        comparison_df : DataFrame
            Comparison of runs
        """
        
        runs_data = []
        
        for run_id in run_ids:
            run = mlflow.get_run(run_id)
            runs_data.append({
                'run_id': run_id,
                'model_type': run.data.params.get('model_type', 'unknown'),
                'feature_stage': run.data.params.get('feature_stage', 'unknown'),
                'mae': run.data.metrics.get('mae', None),
                'rmse': run.data.metrics.get('rmse', None),
                'r2_score': run.data.metrics.get('r2_score', None),
                'date': run.info.start_time
            })
        
        comparison_df = pd.DataFrame(runs_data)
        print("\n✓ Run comparison:")
        print(comparison_df.to_string(index=False))
        
        return comparison_df


def log_best_model_to_mlflow():
    """
    Train and log the best Random Forest model to MLflow.
    """
    
    import sys
    from pathlib import Path
    
    # Add stage3/ML_models to path using absolute path
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(PROJECT_ROOT / 'stage3' / 'ML_models'))
    
    from Best_model import train_best_random_forest, data  # type: ignore
    from Config import RANDOM_FOREST_PARAMS  # type: ignore
    from Feature_Engineering import FeatureSelector  # type: ignore
    
    print("\n" + "="*70)
    print("LOGGING BEST MODEL TO MLFLOW")
    print("="*70)
    
    # Initialize tracker
    tracker = MLflowTracker()
    
    # Train model
    model, metrics = train_best_random_forest(data, 'Weekly_Sales', None)
    
    # Get features
    feature_selector = FeatureSelector()
    features = feature_selector.get_features_by_stage('full')
    
    # Additional info
    additional_info = {
        'dataset': 'Walmart Sales Forecasting',
        'data_shape': data.shape,
        'date_range': f"{data['Date'].min()} to {data['Date'].max()}",
        'stores': int(data['Store'].nunique()),
        'departments': int(data['Dept'].nunique())
    }
    
    # Log to MLflow
    run_id = tracker.log_model_training(
        model=model,
        metrics=metrics,
        params=RANDOM_FOREST_PARAMS,
        features=features,
        model_name="random_forest",
        stage="full",
        additional_info=additional_info
    )
    
    # Log feature importance
    tracker.log_feature_importance(model, features)
    
    print("\n" + "="*70)
    print("MLflow logging complete!")
    print(f"View results: mlflow ui --port 5000")
    print("="*70)
    
    return run_id, model


if __name__ == "__main__":
    # Example usage
    log_best_model_to_mlflow()
