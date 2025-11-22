"""
Performance Tracking System
Monitors model performance metrics over time
"""

import pandas as pd
import numpy as np
from datetime import datetime
import json
from pathlib import Path
from collections import defaultdict


class PerformanceTracker:
    """
    Tracks model performance metrics and predictions over time.
    """
    
    def __init__(self, log_dir='../monitoring/logs'):
        """
        Initialize performance tracker.
        
        Parameters:
        -----------
        log_dir : str
            Directory to store performance logs
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.metrics_log_file = self.log_dir / 'performance_metrics.jsonl'
        self.predictions_log_file = self.log_dir / 'predictions.jsonl'
        
        # Baseline metrics (from training)
        self.baseline_metrics = {
            'mae': 106.77,
            'rmse': 144.53,
            'r2_score': 0.9996
        }
        
        print(f"✓ Performance tracker initialized")
        print(f"  Log directory: {self.log_dir}")
    
    def log_prediction(self, input_data, prediction, actual=None):
        """
        Log a single prediction.
        
        Parameters:
        -----------
        input_data : dict
            Input features
        prediction : float
            Predicted value
        actual : float, optional
            Actual value (if available)
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'Store': input_data.get('Store'),
            'Dept': input_data.get('Dept'),
            'Date': input_data.get('Date'),
            'predicted_sales': float(prediction),
            'actual_sales': float(actual) if actual is not None else None,
            'error': float(actual - prediction) if actual is not None else None,
            'absolute_error': float(abs(actual - prediction)) if actual is not None else None
        }
        
        # Append to log file
        with open(self.predictions_log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def log_batch_predictions(self, predictions_df):
        """
        Log batch predictions.
        
        Parameters:
        -----------
        predictions_df : DataFrame
            DataFrame with predictions and actuals
        """
        for _, row in predictions_df.iterrows():
            self.log_prediction(
                input_data={'Store': row.get('Store'), 'Dept': row.get('Dept'), 'Date': row.get('Date')},
                prediction=row['predicted_sales'],
                actual=row.get('actual_sales')
            )
    
    def calculate_metrics(self, days=7):
        """
        Calculate performance metrics for recent predictions.
        
        Parameters:
        -----------
        days : int
            Number of days to analyze
        
        Returns:
        --------
        metrics : dict
            Performance metrics
        """
        # Load recent predictions
        predictions = self.load_predictions(days=days)
        
        if predictions.empty or predictions['actual_sales'].isna().all():
            return {
                'status': 'insufficient_data',
                'message': 'Not enough predictions with actual values'
            }
        
        # Filter to records with actuals
        valid_preds = predictions.dropna(subset=['actual_sales'])
        
        if len(valid_preds) == 0:
            return {
                'status': 'no_actuals',
                'message': 'No predictions with actual values found'
            }
        
        # Calculate metrics
        mae = np.mean(valid_preds['absolute_error'])
        rmse = np.sqrt(np.mean(valid_preds['error'] ** 2))
        
        # R² score
        ss_res = np.sum(valid_preds['error'] ** 2)
        ss_tot = np.sum((valid_preds['actual_sales'] - valid_preds['actual_sales'].mean()) ** 2)
        r2 = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'period_days': days,
            'num_predictions': len(valid_preds),
            'mae': float(mae),
            'rmse': float(rmse),
            'r2_score': float(r2),
            'baseline_mae': self.baseline_metrics['mae'],
            'baseline_rmse': self.baseline_metrics['rmse'],
            'baseline_r2': self.baseline_metrics['r2_score'],
            'mae_change': float(mae - self.baseline_metrics['mae']),
            'mae_change_pct': float((mae - self.baseline_metrics['mae']) / self.baseline_metrics['mae'] * 100),
            'r2_change': float(r2 - self.baseline_metrics['r2_score']),
            'status': 'healthy' if r2 > 0.90 else 'degraded'
        }
        
        # Log metrics
        with open(self.metrics_log_file, 'a') as f:
            f.write(json.dumps(metrics) + '\n')
        
        return metrics
    
    def load_predictions(self, days=None):
        """
        Load recent predictions from log file.
        
        Parameters:
        -----------
        days : int, optional
            Number of days to load
        
        Returns:
        --------
        predictions_df : DataFrame
            Recent predictions
        """
        if not self.predictions_log_file.exists():
            return pd.DataFrame()
        
        # Load all predictions
        predictions = []
        with open(self.predictions_log_file, 'r') as f:
            for line in f:
                predictions.append(json.loads(line))
        
        df = pd.DataFrame(predictions)
        
        if df.empty:
            return df
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter by days if specified
        if days:
            cutoff = datetime.now() - pd.Timedelta(days=days)
            df = df[df['timestamp'] >= cutoff]
        
        return df
    
    def load_metrics_history(self, days=30):
        """
        Load metrics history.
        
        Parameters:
        -----------
        days : int
            Number of days to load
        
        Returns:
        --------
        metrics_df : DataFrame
            Metrics history
        """
        if not self.metrics_log_file.exists():
            return pd.DataFrame()
        
        # Load all metrics
        metrics = []
        with open(self.metrics_log_file, 'r') as f:
            for line in f:
                metrics.append(json.loads(line))
        
        df = pd.DataFrame(metrics)
        
        if df.empty:
            return df
        
        # Convert timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter by days
        cutoff = datetime.now() - pd.Timedelta(days=days)
        df = df[df['timestamp'] >= cutoff]
        
        return df
    
    def get_performance_summary(self, days=7):
        """
        Get performance summary for dashboard.
        
        Parameters:
        -----------
        days : int
            Number of days to analyze
        
        Returns:
        --------
        summary : dict
            Performance summary
        """
        metrics = self.calculate_metrics(days=days)
        predictions = self.load_predictions(days=days)
        
        summary = {
            'current_metrics': metrics,
            'total_predictions': len(predictions),
            'predictions_with_actuals': len(predictions.dropna(subset=['actual_sales'])),
            'date_range': {
                'start': predictions['timestamp'].min().isoformat() if not predictions.empty else None,
                'end': predictions['timestamp'].max().isoformat() if not predictions.empty else None
            }
        }
        
        return summary
    
    def check_performance_degradation(self, threshold_r2=0.90, threshold_mae_increase=100):
        """
        Check if model performance has degraded.
        
        Parameters:
        -----------
        threshold_r2 : float
            Minimum acceptable R² score
        threshold_mae_increase : float
            Maximum acceptable MAE increase from baseline
        
        Returns:
        --------
        alert : dict
            Alert information if degradation detected
        """
        metrics = self.calculate_metrics(days=7)
        
        if metrics.get('status') in ['insufficient_data', 'no_actuals']:
            return {'alert': False, 'reason': metrics.get('message')}
        
        alerts = []
        
        # Check R² score
        if metrics['r2_score'] < threshold_r2:
            alerts.append({
                'type': 'r2_degradation',
                'severity': 'high',
                'message': f"R² score dropped to {metrics['r2_score']:.4f} (below threshold {threshold_r2})",
                'current_value': metrics['r2_score'],
                'threshold': threshold_r2
            })
        
        # Check MAE increase
        if metrics['mae_change'] > threshold_mae_increase:
            alerts.append({
                'type': 'mae_increase',
                'severity': 'medium',
                'message': f"MAE increased by ${metrics['mae_change']:.2f} (above threshold ${threshold_mae_increase})",
                'current_value': metrics['mae'],
                'baseline': self.baseline_metrics['mae']
            })
        
        return {
            'alert': len(alerts) > 0,
            'alerts': alerts,
            'metrics': metrics
        }


if __name__ == "__main__":
    # Test tracker
    tracker = PerformanceTracker()
    
    # Simulate some predictions
    print("\nSimulating predictions...")
    for i in range(5):
        tracker.log_prediction(
            input_data={'Store': 1, 'Dept': 1, 'Date': '2023-11-22'},
            prediction=15000 + np.random.randn() * 100,
            actual=15000 + np.random.randn() * 150
        )
    
    # Calculate metrics
    print("\nCalculating metrics...")
    metrics = tracker.calculate_metrics(days=7)
    print(json.dumps(metrics, indent=2))
    
    # Check degradation
    print("\nChecking for degradation...")
    alert = tracker.check_performance_degradation()
    print(json.dumps(alert, indent=2))
