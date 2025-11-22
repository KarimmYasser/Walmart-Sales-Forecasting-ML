"""
Data Drift Detection
Detects distribution shifts in input features over time
"""

import pandas as pd
import numpy as np
from datetime import datetime
from scipy import stats
from pathlib import Path
import json


class DriftDetector:
    """
    Detects data drift in features using statistical tests.
    """
    
    def __init__(self, reference_data=None, log_dir='../monitoring/logs'):
        """
        Initialize drift detector.
        
        Parameters:
        -----------
        reference_data : DataFrame, optional
            Reference dataset (training data)
        log_dir : str
            Directory to store drift logs
        """
        self.reference_data = reference_data
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        self.drift_log_file = self.log_dir / 'drift_detection.jsonl'
        
        # Features to monitor
        self.numerical_features = [
            'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Size'
        ]
        
        self.categorical_features = ['Type', 'IsHoliday']
        
        print(f"✓ Drift detector initialized")
    
    def detect_numerical_drift(self, current_data, feature, method='ks_test', threshold=0.05):
        """
        Detect drift in numerical feature using statistical tests.
        
        Parameters:
        -----------
        current_data : DataFrame
            Current data window
        feature : str
            Feature name
        method : str
            Test method ('ks_test', 'mann_whitney')
        threshold : float
            P-value threshold for drift detection
        
        Returns:
        --------
        drift_result : dict
            Drift detection results
        """
        if self.reference_data is None:
            return {'drift_detected': False, 'reason': 'no_reference_data'}
        
        ref_values = self.reference_data[feature].dropna()
        curr_values = current_data[feature].dropna()
        
        if len(ref_values) == 0 or len(curr_values) == 0:
            return {'drift_detected': False, 'reason': 'insufficient_data'}
        
        # Kolmogorov-Smirnov test
        if method == 'ks_test':
            statistic, p_value = stats.ks_2samp(ref_values, curr_values)
            test_name = 'Kolmogorov-Smirnov'
        
        # Mann-Whitney U test
        elif method == 'mann_whitney':
            statistic, p_value = stats.mannwhitneyu(ref_values, curr_values, alternative='two-sided')
            test_name = 'Mann-Whitney U'
        
        else:
            raise ValueError(f"Unknown method: {method}")
        
        drift_detected = p_value < threshold
        
        # Calculate distribution statistics
        ref_stats = {
            'mean': float(ref_values.mean()),
            'std': float(ref_values.std()),
            'median': float(ref_values.median()),
            'min': float(ref_values.min()),
            'max': float(ref_values.max())
        }
        
        curr_stats = {
            'mean': float(curr_values.mean()),
            'std': float(curr_values.std()),
            'median': float(curr_values.median()),
            'min': float(curr_values.min()),
            'max': float(curr_values.max())
        }
        
        result = {
            'feature': feature,
            'feature_type': 'numerical',
            'test': test_name,
            'statistic': float(statistic),
            'p_value': float(p_value),
            'threshold': threshold,
            'drift_detected': drift_detected,
            'reference_stats': ref_stats,
            'current_stats': curr_stats,
            'mean_change': float(curr_stats['mean'] - ref_stats['mean']),
            'mean_change_pct': float((curr_stats['mean'] - ref_stats['mean']) / ref_stats['mean'] * 100) if ref_stats['mean'] != 0 else None
        }
        
        return result
    
    def detect_categorical_drift(self, current_data, feature, threshold=0.05):
        """
        Detect drift in categorical feature using chi-square test.
        
        Parameters:
        -----------
        current_data : DataFrame
            Current data window
        feature : str
            Feature name
        threshold : float
            P-value threshold
        
        Returns:
        --------
        drift_result : dict
            Drift detection results
        """
        if self.reference_data is None:
            return {'drift_detected': False, 'reason': 'no_reference_data'}
        
        ref_dist = self.reference_data[feature].value_counts(normalize=True)
        curr_dist = current_data[feature].value_counts(normalize=True)
        
        # Align distributions
        all_categories = set(ref_dist.index) | set(curr_dist.index)
        ref_freq = [ref_dist.get(cat, 0) * len(self.reference_data) for cat in all_categories]
        curr_freq = [curr_dist.get(cat, 0) * len(current_data) for cat in all_categories]
        
        # Chi-square test
        statistic, p_value = stats.chisquare(curr_freq, ref_freq)
        
        drift_detected = p_value < threshold
        
        result = {
            'feature': feature,
            'feature_type': 'categorical',
            'test': 'Chi-Square',
            'statistic': float(statistic),
            'p_value': float(p_value),
            'threshold': threshold,
            'drift_detected': drift_detected,
            'reference_distribution': {str(k): float(v) for k, v in ref_dist.items()},
            'current_distribution': {str(k): float(v) for k, v in curr_dist.items()}
        }
        
        return result
    
    def detect_all_features(self, current_data, threshold=0.05):
        """
        Detect drift across all features.
        
        Parameters:
        -----------
        current_data : DataFrame
            Current data window
        threshold : float
            P-value threshold
        
        Returns:
        --------
        drift_report : dict
            Complete drift report
        """
        results = []
        drift_count = 0
        
        # Check numerical features
        for feature in self.numerical_features:
            if feature in current_data.columns:
                result = self.detect_numerical_drift(current_data, feature, threshold=threshold)
                results.append(result)
                if result.get('drift_detected'):
                    drift_count += 1
        
        # Check categorical features
        for feature in self.categorical_features:
            if feature in current_data.columns:
                result = self.detect_categorical_drift(current_data, feature, threshold=threshold)
                results.append(result)
                if result.get('drift_detected'):
                    drift_count += 1
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'num_features_checked': len(results),
            'num_features_drifted': drift_count,
            'drift_percentage': float(drift_count / len(results) * 100) if len(results) > 0 else 0,
            'overall_drift_detected': drift_count >= 3,  # Alert if 3+ features drift
            'feature_results': results
        }
        
        # Log report
        with open(self.drift_log_file, 'a') as f:
            f.write(json.dumps(report) + '\n')
        
        return report
    
    def get_drift_summary(self, days=7):
        """
        Get drift detection summary.
        
        Parameters:
        -----------
        days : int
            Number of days to analyze
        
        Returns:
        --------
        summary : dict
            Drift summary
        """
        if not self.drift_log_file.exists():
            return {'status': 'no_data', 'message': 'No drift detection logs found'}
        
        # Load recent drift logs
        reports = []
        with open(self.drift_log_file, 'r') as f:
            for line in f:
                reports.append(json.loads(line))
        
        df = pd.DataFrame(reports)
        
        if df.empty:
            return {'status': 'no_data', 'message': 'No drift reports available'}
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        cutoff = datetime.now() - pd.Timedelta(days=days)
        recent_df = df[df['timestamp'] >= cutoff]
        
        if recent_df.empty:
            return {'status': 'no_recent_data', 'message': f'No drift reports in last {days} days'}
        
        summary = {
            'period_days': days,
            'num_checks': len(recent_df),
            'drift_alerts': int(recent_df['overall_drift_detected'].sum()),
            'avg_drifted_features': float(recent_df['num_features_drifted'].mean()),
            'max_drifted_features': int(recent_df['num_features_drifted'].max()),
            'latest_check': recent_df['timestamp'].max().isoformat(),
            'status': 'healthy' if recent_df['overall_drift_detected'].sum() == 0 else 'drift_detected'
        }
        
        return summary


if __name__ == "__main__":
    # Test drift detector
    print("Drift Detector Test")
    
    # Create sample reference data
    np.random.seed(42)
    ref_data = pd.DataFrame({
        'Temperature': np.random.normal(60, 10, 1000),
        'Fuel_Price': np.random.normal(3.5, 0.5, 1000),
        'Type': np.random.choice(['A', 'B', 'C'], 1000),
        'IsHoliday': np.random.choice([True, False], 1000, p=[0.05, 0.95])
    })
    
    # Create sample current data (with slight drift)
    curr_data = pd.DataFrame({
        'Temperature': np.random.normal(65, 12, 100),  # Drift in mean and std
        'Fuel_Price': np.random.normal(3.5, 0.5, 100),  # No drift
        'Type': np.random.choice(['A', 'B', 'C'], 100),
        'IsHoliday': np.random.choice([True, False], 100, p=[0.05, 0.95])
    })
    
    detector = DriftDetector(reference_data=ref_data)
    report = detector.detect_all_features(curr_data)
    
    print("\n" + "="*70)
    print(f"Drift Detection Report")
    print("="*70)
    print(f"Features Checked: {report['num_features_checked']}")
    print(f"Features Drifted: {report['num_features_drifted']}")
    print(f"Overall Drift: {report['overall_drift_detected']}")
    
    print("\nFeature Details:")
    for result in report['feature_results']:
        status = "DRIFT" if result.get('drift_detected') else "OK"
        print(f"  {result['feature']}: {status} (p-value: {result.get('p_value', 'N/A')})")
