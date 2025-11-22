"""
Model Registry and Version Management
Manages model versions, stages (staging/production), and metadata
"""

import mlflow
from mlflow.tracking import MlflowClient
from datetime import datetime
import pandas as pd


class ModelRegistry:
    """
    Manages model versions and lifecycle stages in MLflow Model Registry.
    """
    
    def __init__(self, tracking_uri="./mlruns"):
        """
        Initialize Model Registry client.
        
        Parameters:
        -----------
        tracking_uri : str
            MLflow tracking URI
        """
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()
        print(f"✓ Model Registry initialized")
    
    def register_model(self, run_id, model_name="sales_forecaster"):
        """
        Register a model from a run.
        
        Parameters:
        -----------
        run_id : str
            MLflow run ID
        model_name : str
            Name for registered model
        
        Returns:
        --------
        model_version : ModelVersion
            Registered model version
        """
        
        model_uri = f"runs:/{run_id}/model"
        
        model_version = mlflow.register_model(model_uri, model_name)
        
        print(f"\n✓ Model registered")
        print(f"  Name: {model_name}")
        print(f"  Version: {model_version.version}")
        
        return model_version
    
    def transition_model_stage(self, model_name, version, stage):
        """
        Transition model to a new stage.
        
        Parameters:
        -----------
        model_name : str
            Registered model name
        version : int
            Model version number
        stage : str
            Target stage: 'Staging', 'Production', 'Archived'
        """
        
        self.client.transition_model_version_stage(
            name=model_name,
            version=version,
            stage=stage
        )
        
        print(f"\n✓ Model transitioned")
        print(f"  Model: {model_name} v{version}")
        print(f"  Stage: {stage}")
    
    def get_latest_production_model(self, model_name="sales_forecaster"):
        """
        Get the latest production model.
        
        Parameters:
        -----------
        model_name : str
            Registered model name
        
        Returns:
        --------
        model : sklearn model
            Production model
        version : int
            Model version
        """
        
        model_uri = f"models:/{model_name}/Production"
        
        try:
            model = mlflow.sklearn.load_model(model_uri)
            
            # Get version info
            versions = self.client.get_latest_versions(model_name, stages=["Production"])
            version = versions[0].version if versions else "unknown"
            
            print(f"\n✓ Production model loaded")
            print(f"  Model: {model_name}")
            print(f"  Version: {version}")
            
            return model, version
        
        except Exception as e:
            print(f"Error loading production model: {e}")
            return None, None
    
    def list_model_versions(self, model_name="sales_forecaster"):
        """
        List all versions of a model.
        
        Parameters:
        -----------
        model_name : str
            Registered model name
        
        Returns:
        --------
        versions_df : DataFrame
            Information about all versions
        """
        
        try:
            versions = self.client.search_model_versions(f"name='{model_name}'")
            
            versions_data = []
            for v in versions:
                versions_data.append({
                    'version': v.version,
                    'stage': v.current_stage,
                    'run_id': v.run_id,
                    'created': datetime.fromtimestamp(v.creation_timestamp/1000),
                    'status': v.status
                })
            
            versions_df = pd.DataFrame(versions_data).sort_values('version', ascending=False)
            
            print(f"\n✓ Model versions for {model_name}:")
            print(versions_df.to_string(index=False))
            
            return versions_df
        
        except Exception as e:
            print(f"Error listing versions: {e}")
            return pd.DataFrame()
    
    def add_model_description(self, model_name, version, description):
        """
        Add description to a model version.
        
        Parameters:
        -----------
        model_name : str
            Registered model name
        version : int
            Model version
        description : str
            Description text
        """
        
        self.client.update_model_version(
            name=model_name,
            version=version,
            description=description
        )
        
        print(f"✓ Description added to {model_name} v{version}")
    
    def compare_models(self, model_name="sales_forecaster", stages=['Staging', 'Production']):
        """
        Compare models across different stages.
        
        Parameters:
        -----------
        model_name : str
            Registered model name
        stages : list
            Stages to compare
        
        Returns:
        --------
        comparison_df : DataFrame
            Comparison results
        """
        
        comparison_data = []
        
        for stage in stages:
            versions = self.client.get_latest_versions(model_name, stages=[stage])
            
            if versions:
                v = versions[0]
                run = self.client.get_run(v.run_id)
                
                comparison_data.append({
                    'stage': stage,
                    'version': v.version,
                    'mae': run.data.metrics.get('mae', None),
                    'rmse': run.data.metrics.get('rmse', None),
                    'r2_score': run.data.metrics.get('r2_score', None),
                    'run_id': v.run_id
                })
        
        comparison_df = pd.DataFrame(comparison_data)
        
        if not comparison_df.empty:
            print(f"\n✓ Model comparison:")
            print(comparison_df.to_string(index=False))
        
        return comparison_df


if __name__ == "__main__":
    # Example usage
    registry = ModelRegistry()
    
    # List all versions
    registry.list_model_versions()
    
    # Load production model
    model, version = registry.get_latest_production_model()
