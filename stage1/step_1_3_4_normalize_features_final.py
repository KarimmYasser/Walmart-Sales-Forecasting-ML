"""
MILESTONE 1 - Step 1.3.4: Normalize Numerical Features
======================================================
Task 3: Preprocessing and Feature Engineering (Final Step)

Normalize numerical features to standardize ranges for ML models.
Using manual Z-score normalization (no sklearn dependency).

"""

import pandas as pd
import numpy as np
import os
import json

print("="*80)
print("STEP 1.3.4: NORMALIZE NUMERICAL FEATURES")
print("="*80)

print("\n[1] Loading encoded data...")
train = pd.read_csv('processed_data/Stage1.3.3/train_encoded.csv')
test = pd.read_csv('processed_data/Stage1.3.3/test_encoded.csv')
print(f"Loaded: train {train.shape}, test {test.shape}")

continuous_features = [
    'Size', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment',
    'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5',
    'Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4', 'Sales_Rolling_Mean_4',
    'Sales_Rolling_Mean_8', 'Sales_Rolling_Std_4', 'Sales_Momentum'
]

print("\n[2] Calculating normalization parameters...")
normalization_params = {}
for feature in continuous_features:
    if feature in train.columns:
        mean_val = train[feature].mean()
        std_val = train[feature].std()
        normalization_params[feature] = {'mean': mean_val, 'std': std_val}
print(f"Calculated parameters for {len(normalization_params)} features")

print("\n[3] Applying Z-score normalization...")
for feature in continuous_features:
    if feature in train.columns:
        mean_val = normalization_params[feature]['mean']
        std_val = normalization_params[feature]['std']
        if std_val > 0:
            train[feature] = (train[feature] - mean_val) / std_val
        else:
            train[feature] = 0
            
for feature in continuous_features:
    if feature in test.columns:
        mean_val = normalization_params[feature]['mean']
        std_val = normalization_params[feature]['std']
        if std_val > 0:
            test[feature] = (test[feature] - mean_val) / std_val
        else:
            test[feature] = 0
print("Normalized train and test data")

print("\n[4] Saving normalization parameters and data...")
output_dir = 'processed_data/Stage1.3.4_Final'
os.makedirs(output_dir, exist_ok=True)

params_path = os.path.join(output_dir, 'normalization_params.json')
with open(params_path, 'w') as f:
    json.dump(normalization_params, f, indent=2)

train_output = os.path.join(output_dir, 'train_final.csv')
test_output = os.path.join(output_dir, 'test_final.csv')
train.to_csv(train_output, index=False)
test.to_csv(test_output, index=False)
print(f"Saved: {train_output}, {test_output}, {params_path}")

print("\n" + "="*80)
print("STEP 1.3.4 COMPLETED!")
print("="*80)
