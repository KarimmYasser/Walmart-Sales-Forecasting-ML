# The best-performing sales and demand forecasting model, ready for deployment

import pandas as pd
import numpy as np
from datetime import datetime
import pickle
from Config import RANDOM_FOREST_PARAMS, TRAIN_TEST_SPLIT_RATIO
from Feature_Engineering import FeatureSelector
from Evaluation import ModelEvaluator
from Models import ModelTrainer

# data
data = pd.read_csv(r"D:\Downloads\Depi_project_Data-science\stage1\processed_data\Stage1.3.4_Final\train_final.csv")

# Trains the best Random Forest model using all features and evaluates its performance.
def train_best_random_forest(data, target_col='Weekly_Sales', save_path=None):

    print("\n" + "="*70)
    print("TRAINING BEST MODEL: RANDOM FOREST (FULL FEATURES)")
    print("="*70)
    
    # Initialize components
    feature_selector = FeatureSelector()
    model_trainer = ModelTrainer()
    evaluator = ModelEvaluator()
    
    # Get all features
    features = feature_selector.get_features_by_stage('full')
    print(f"\nFeatures selected: {len(features)} features")
    print(f"Features: {', '.join(features[:5])}...")
    
    # Prepare data
    print("\nPreparing data...")
    data_sorted = data.sort_values('Date').reset_index(drop=True)
    
    X = data_sorted[features]
    y = data_sorted[target_col]
    
    # Time series split
    split_idx = int(len(X) * TRAIN_TEST_SPLIT_RATIO)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    
    print(f"Train samples: {len(X_train):,}")
    print(f"Test samples: {len(X_test):,}")
    
    # Train Random Forest
    print("\n" + "-"*70)
    print("Training Random Forest model...")
    print("-"*70)
    
    model, predictions, metrics = model_trainer.train_random_forest(
        X_train, y_train, X_test, y_test
    )
    
    # Print results
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)

    print(f"Model Type: Random Forest")
    print(f"Features: {len(features)}")

    print(f"\nPerformance Metrics:")
    print(f"  MAE:  ${metrics['MAE']:,.2f}")
    print(f"  RMSE: ${metrics['RMSE']:,.2f}")
    print(f"  R²:   {metrics['R2']:.4f} ({metrics['R2']*100:.2f})")
    
    # Rating
    if metrics['R2'] >= 0.95:
        rating = "EXCELLENT "
    elif metrics['R2'] >= 0.90:
        rating = "VERY GOOD "
    elif metrics['R2'] >= 0.85:
        rating = "GOOD "
    else:
        rating = "ACCEPTABLE "

    print(f"\nPerformance Rating: {rating}")
    print(f"Status: {'APPROVED FOR PRODUCTION' if metrics['R2'] >= 0.90 else 'NEEDS REVIEW'}")

# Save model if path provided
    if save_path:
        print(f"\nSaving model to: {save_path}")
        with open(save_path, 'wb') as f:
            pickle.dump(model, f)
        print("✓ Model saved successfully")
    
    print("="*70 + "\n")
    
    # Return model and metrics (IMPORTANT!)
    return model, metrics


def Best_model_results(save_model=False, save_path='best_rf_model.pkl'):
    """
    Train and return the best Random Forest model.
    
    Parameters:
    -----------
    save_model : bool
        Whether to save the model to disk
    save_path : str
        Path to save the model (if save_model=True)
    
    Returns:
    --------
    tuple : (model, metrics)
    """
    if save_model:
        model, metrics = train_best_random_forest(data, 'Weekly_Sales', save_path)
    else:
        model, metrics = train_best_random_forest(data, 'Weekly_Sales', None)
    
    return model, metrics



# Option 2: Train, get model, and save to file
# model, metrics = Best_model_results(save_model=True, save_path='my_model.pkl')

# Option 3: Use the model for predictions
# model, metrics = Best_model_results()
# predictions = model.predict(new_data)

if __name__ == "__main__":
    # Run the training
    model, metrics = Best_model_results(save_model=True)
    print(f"\nModel ready to use!")
    print(f"MAE: ${metrics['MAE']:.2f}")
    print(f"R²: {metrics['R2']:.4f}")    