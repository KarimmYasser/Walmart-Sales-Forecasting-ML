"""
Predictor class for handling model predictions
Loads model and performs inference with feature engineering
"""

import pandas as pd
import numpy as np
import pickle
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add stage3 to path for imports using absolute path
PROJECT_ROOT = Path(__file__).parent.parent.parent
stage3_path = str(PROJECT_ROOT / 'stage3' / 'ML_models')
if stage3_path not in sys.path:
    sys.path.insert(0, stage3_path)

from Feature_Engineering import FeatureSelector  # type: ignore


class SalesPredictor:
    """
    Handles loading model and making predictions with proper feature engineering.
    """
    
    def __init__(self, model_path='../models/best_model.pkl'):
        """
        Initialize predictor and load model.
        
        Parameters:
        -----------
        model_path : str
            Path to saved model file
        """
        self.model = None
        self.feature_selector = FeatureSelector()
        self.features = self.feature_selector.get_features_by_stage('full')
        self.model_path = model_path
        self.historical_data = None
        
        # Load historical data for lag features
        self._load_historical_data()
        
        # Load model
        self.load_model()
        
        # Store metadata
        self.model_info = {
            'model_type': 'Random Forest',
            'version': '1.0',
            'features_count': len(self.features),
            'last_trained': '2024-11-22',
            'performance': {
                'mae': 106.77,
                'rmse': 144.53,
                'r2_score': 0.9996
            }
        }
    
    def load_model(self):
        """Load the trained model from disk."""
        try:
            model_file = Path(self.model_path)
            
            # Check if model exists
            if not model_file.exists():
                print(f"⚠ Model file not found at {model_file}")
                print("  Attempting to train model...")
                self._train_and_save_model()
                
                # Try loading again
                if model_file.exists():
                    with open(model_file, 'rb') as f:
                        self.model = pickle.load(f)
                    print(f"✓ Model loaded from {model_file}")
                else:
                    print("⚠ Using mock model for demonstration")
            else:
                # Load model
                with open(model_file, 'rb') as f:
                    self.model = pickle.load(f)
                print(f"✓ Model loaded from {model_file}")
            
        except Exception as e:
            print(f"✗ Error loading model: {e}")
            print("⚠ Using mock model for demonstration")
            self._create_mock_model()
    
    def _train_and_save_model(self):
        """Train and save model if it doesn't exist."""
        try:
            import sys
            from pathlib import Path
            
            # Add stage3/ML_models to path for importing Best_model
            stage3_ml_path = Path(__file__).parent.parent.parent / 'stage3' / 'ML_models'
            if str(stage3_ml_path) not in sys.path:
                sys.path.insert(0, str(stage3_ml_path))
            
            from Best_model import train_best_random_forest, data  # type: ignore
            
            print("Training best model...")
            model, metrics = train_best_random_forest(data, 'Weekly_Sales', None)
            
            # Save model
            model_dir = Path(self.model_path).parent
            model_dir.mkdir(parents=True, exist_ok=True)
            
            with open(self.model_path, 'wb') as f:
                pickle.dump(model, f)
            
            print(f"✓ Model saved to {self.model_path}")
        except Exception as e:
            print(f"⚠ Could not train model: {e}")
            print("  Creating a mock model for demonstration...")
            self._create_mock_model()
    
    def _create_mock_model(self):
        """Create a simple mock model for demonstration when real model can't be loaded."""
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.datasets import make_regression
        
        print("Creating mock model for demonstration...")
        
        # Create simple mock data
        X, y = make_regression(n_samples=100, n_features=44, noise=0.1, random_state=42)
        
        # Train simple model
        self.model = RandomForestRegressor(n_estimators=10, max_depth=5, random_state=42)
        self.model.fit(X, y * 15000)  # Scale to typical sales values
        
        # Save mock model
        model_dir = Path(self.model_path).parent
        model_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        print(f"✓ Mock model created and saved to {self.model_path}")
        print("⚠ Note: This is a demonstration model with simulated predictions")
    
    def _load_historical_data(self):
        """Load historical sales data for calculating lag features."""
        try:
            data_path = Path(__file__).parent.parent.parent / 'stage1' / 'processed_data' / 'Stage1.3.4_Final' / 'train_final.csv'
            if data_path.exists():
                # Load only necessary columns to save memory
                self.historical_data = pd.read_csv(
                    data_path, 
                    usecols=['Store', 'Dept', 'Date', 'Weekly_Sales'],
                    parse_dates=['Date']
                )
                # Keep only recent data (last 3 months of training data)
                self.historical_data = self.historical_data.sort_values('Date').tail(50000)
                print(f"✓ Loaded {len(self.historical_data):,} historical records for lag features")
            else:
                print(f"⚠ Historical data not found at {data_path}")
                self.historical_data = None
        except Exception as e:
            print(f"⚠ Could not load historical data: {e}")
            self.historical_data = None
    
    def _get_historical_sales(self, store, dept, date):
        """Get historical sales for a specific store/dept to calculate lag features."""
        if self.historical_data is None:
            return None
        
        try:
            # Convert date to datetime if it's a string
            if isinstance(date, str):
                pred_date = pd.to_datetime(date)
            else:
                pred_date = pd.to_datetime(date)
            
            # Filter for this store and department, AND before prediction date
            store_dept_data = self.historical_data[
                (self.historical_data['Store'] == store) & 
                (self.historical_data['Dept'] == dept) &
                (self.historical_data['Date'] < pred_date)
            ].sort_values('Date')
            
            if len(store_dept_data) == 0:
                return None
            
            # Get sales from most recent weeks BEFORE the prediction date
            recent_sales = store_dept_data['Weekly_Sales'].tail(8).values
            
            if len(recent_sales) >= 4:
                return {
                    'lag1': recent_sales[-1] if len(recent_sales) >= 1 else None,
                    'lag2': recent_sales[-2] if len(recent_sales) >= 2 else None,
                    'lag4': recent_sales[-4] if len(recent_sales) >= 4 else None,
                    'rolling_mean_4': recent_sales[-4:].mean() if len(recent_sales) >= 4 else None,
                    'rolling_mean_8': recent_sales.mean() if len(recent_sales) >= 8 else recent_sales.mean(),
                    'rolling_std_4': recent_sales[-4:].std() if len(recent_sales) >= 4 else None,
                    'momentum': (recent_sales[-1] - recent_sales[-4]) if len(recent_sales) >= 4 else 0
                }
            
            return None
        except Exception as e:
            print(f"Error getting historical sales: {e}")
            return None
    
    def engineer_features(self, input_data):
        """
        Create all required features from input data.
        
        Parameters:
        -----------
        input_data : dict or DataFrame
            Raw input data
        
        Returns:
        --------
        features_df : DataFrame
            Engineered features ready for prediction
        """
        # Convert to DataFrame if dict
        if isinstance(input_data, dict):
            df = pd.DataFrame([input_data])
        else:
            df = input_data.copy()
        
        # Convert Date to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Extract time features
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        df['WeekOfYear'] = df['Date'].dt.isocalendar().week
        df['Quarter'] = df['Date'].dt.quarter
        
        # Cyclical encoding
        df['Month_Sin'] = np.sin(2 * np.pi * df['Month'] / 12)
        df['Month_Cos'] = np.cos(2 * np.pi * df['Month'] / 12)
        df['Week_Sin'] = np.sin(2 * np.pi * df['WeekOfYear'] / 52)
        df['Week_Cos'] = np.cos(2 * np.pi * df['WeekOfYear'] / 52)
        df['DayOfWeek_Sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
        df['DayOfWeek_Cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)
        
        # Boolean time features
        df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
        df['Is_Month_Start'] = (df['Date'].dt.is_month_start).astype(int)
        df['Is_Month_End'] = (df['Date'].dt.is_month_end).astype(int)
        df['Is_Quarter_Start'] = (df['Date'].dt.is_quarter_start).astype(int)
        df['Is_Quarter_End'] = (df['Date'].dt.is_quarter_end).astype(int)
        df['Is_Year_Start'] = (df['Date'].dt.is_year_start).astype(int)
        df['Is_Year_End'] = (df['Date'].dt.is_year_end).astype(int)
        
        # Encode store type
        df['Type_A'] = (df['Type'] == 'A').astype(int)
        df['Type_B'] = (df['Type'] == 'B').astype(int)
        df['Type_C'] = (df['Type'] == 'C').astype(int)
        
        # Handle markdown features (set to 0 if not provided)
        for i in range(1, 6):
            markdown_col = f'MarkDown{i}'
            if markdown_col not in df.columns:
                df[markdown_col] = 0
            df[f'Has_MarkDown{i}'] = (df[markdown_col] > 0).astype(int)
        
        # Lag features - Try to get from historical data first
        store = df['Store'].values[0]
        dept = df['Dept'].values[0]
        historical_sales = self._get_historical_sales(store, dept, df['Date'].values[0])
        
        if historical_sales is not None:
            # Use real historical data
            df['Sales_Lag1'] = df.get('Sales_Lag1', historical_sales['lag1'])
            df['Sales_Lag2'] = df.get('Sales_Lag2', historical_sales['lag2'])
            df['Sales_Lag4'] = df.get('Sales_Lag4', historical_sales['lag4'])
            df['Sales_Rolling_Mean_4'] = df.get('Sales_Rolling_Mean_4', historical_sales['rolling_mean_4'])
            df['Sales_Rolling_Mean_8'] = df.get('Sales_Rolling_Mean_8', historical_sales['rolling_mean_8'])
            df['Sales_Rolling_Std_4'] = df.get('Sales_Rolling_Std_4', historical_sales['rolling_std_4'])
            df['Sales_Momentum'] = df.get('Sales_Momentum', historical_sales['momentum'])
        else:
            # Fallback: Calculate based on store/dept characteristics
            base_sales = df['Size'].values[0] * 0.03
            
            # Adjust by store type
            if df['Type_A'].values[0] == 1:
                base_sales *= 1.3
            elif df['Type_B'].values[0] == 1:
                base_sales *= 1.0
            else:  # Type C
                base_sales *= 0.7
            
            # Adjust by department
            dept_factor = 1.0 + (dept % 10) * 0.1
            base_sales *= dept_factor
            
            # Add seasonal variation
            month_factor = 1.0 + 0.3 * np.sin(2 * np.pi * df['Month'].values[0] / 12)
            base_sales *= month_factor
            
            # Holiday boost
            if df['IsHoliday'].values[0] == 1:
                base_sales *= 1.5
            
            # Add variation based on store/dept/date
            seed_val = int(store * 1000 + dept * 100 + df['Month'].values[0] * 10 + df['Day'].values[0])
            np.random.seed(seed_val)
            variation = np.random.uniform(0.8, 1.2)
            base_sales *= variation
            
            df['Sales_Lag1'] = df.get('Sales_Lag1', base_sales)
            df['Sales_Lag2'] = df.get('Sales_Lag2', base_sales * 0.95)
            df['Sales_Lag4'] = df.get('Sales_Lag4', base_sales * 0.92)
            df['Sales_Rolling_Mean_4'] = df.get('Sales_Rolling_Mean_4', base_sales * 0.98)
            df['Sales_Rolling_Mean_8'] = df.get('Sales_Rolling_Mean_8', base_sales * 0.97)
            df['Sales_Rolling_Std_4'] = df.get('Sales_Rolling_Std_4', base_sales * 0.15)
            df['Sales_Momentum'] = df.get('Sales_Momentum', base_sales * 0.03)
        
        # Fill missing economic indicators with provided values or defaults
        df['CPI'] = df.get('CPI', df.get('CPI', 211.0))
        df['Unemployment'] = df.get('Unemployment', df.get('Unemployment', 7.5))
        
        # Convert IsHoliday to int
        df['IsHoliday'] = df['IsHoliday'].astype(int)
        
        # Select only required features
        feature_df = df[self.features]
        
        return feature_df
    
    def predict_single(self, input_data):
        """
        Make a single prediction.
        
        Parameters:
        -----------
        input_data : dict
            Input features
        
        Returns:
        --------
        prediction : dict
            Prediction with confidence interval
        """
        # Engineer features
        features = self.engineer_features(input_data)
        
        # Debug: Print key feature values to verify they're different
        print(f"\n🔍 Prediction Debug for Store {input_data['Store']}, Dept {input_data['Dept']}:")
        print(f"   Lag Features: Lag1={features['Sales_Lag1'].values[0]:.2f}, "
              f"Lag2={features['Sales_Lag2'].values[0]:.2f}, "
              f"Lag4={features['Sales_Lag4'].values[0]:.2f}")
        print(f"   Rolling Mean: {features['Sales_Rolling_Mean_4'].values[0]:.2f}")
        print(f"   Size: {features['Size'].values[0]}, IsHoliday: {features['IsHoliday'].values[0]}")
        
        # Make prediction using the trained model
        prediction_value = self.model.predict(features)[0]
        
        print(f"   ✅ Model Output: ${prediction_value:,.2f}")
        
        # Calculate confidence interval (rough estimate)
        mae = 106.77  # From training
        ci_lower = max(0, prediction_value - (1.96 * mae))
        ci_upper = prediction_value + (1.96 * mae)
        
        return {
            'predicted_sales': float(prediction_value),
            'ci_lower': float(ci_lower),
            'ci_upper': float(ci_upper),
            'Store': input_data['Store'],
            'Dept': input_data['Dept'],
            'Date': input_data['Date']
        }
    
    def predict_batch(self, input_data_list):
        """
        Make batch predictions.
        
        Parameters:
        -----------
        input_data_list : list of dict
            List of input records
        
        Returns:
        --------
        predictions : list of dict
            Predictions for all records
        """
        # Convert to DataFrame
        df = pd.DataFrame(input_data_list)
        
        # Engineer features
        features = self.engineer_features(df)
        
        # Make predictions
        predictions = self.model.predict(features)
        
        # Format results
        results = []
        mae = 106.77
        
        for i, pred in enumerate(predictions):
            results.append({
                'predicted_sales': float(pred),
                'ci_lower': float(max(0, pred - (1.96 * mae))),
                'ci_upper': float(pred + (1.96 * mae)),
                'Store': input_data_list[i]['Store'],
                'Dept': input_data_list[i]['Dept'],
                'Date': input_data_list[i]['Date']
            })
        
        return results
    
    def predict_store_forecast(self, store_id, date, top_n=10):
        """Predict for top departments in a store."""
        # Example implementation - would need historical data
        predictions = []
        top_depts = [1, 2, 3, 7, 8, 14, 16, 38, 72, 92][:top_n]
        
        for dept in top_depts:
            input_data = {
                'Store': store_id,
                'Dept': dept,
                'Date': date,
                'IsHoliday': False,
                'Temperature': 60.0,
                'Fuel_Price': 3.5,
                'Type': 'A',
                'Size': 150000
            }
            pred = self.predict_single(input_data)
            predictions.append(pred)
        
        return predictions
    
    def predict_multi_week(self, store_id, dept_id, start_date, weeks=4):
        """Predict for multiple weeks ahead."""
        predictions = []
        start = datetime.strptime(start_date, '%Y-%m-%d')
        
        for week in range(weeks):
            pred_date = start + timedelta(weeks=week)
            
            input_data = {
                'Store': store_id,
                'Dept': dept_id,
                'Date': pred_date.strftime('%Y-%m-%d'),
                'IsHoliday': False,
                'Temperature': 60.0,
                'Fuel_Price': 3.5,
                'Type': 'A',
                'Size': 150000
            }
            pred = self.predict_single(input_data)
            predictions.append(pred)
        
        return predictions
    
    def get_model_info(self):
        """Get model information."""
        return self.model_info
    
    def get_performance_metrics(self):
        """Get performance metrics."""
        return self.model_info['performance']


if __name__ == "__main__":
    # Test predictor
    predictor = SalesPredictor()
    
    # Test prediction
    test_input = {
        'Store': 1,
        'Dept': 1,
        'Date': '2023-11-24',
        'IsHoliday': True,
        'Temperature': 42.31,
        'Fuel_Price': 2.572,
        'CPI': 211.096,
        'Unemployment': 8.106,
        'Type': 'A',
        'Size': 151315
    }
    
    result = predictor.predict_single(test_input)
    print(f"\nPrediction: ${result['predicted_sales']:,.2f}")
    print(f"Confidence Interval: ${result['ci_lower']:,.2f} - ${result['ci_upper']:,.2f}")
