"""
MILESTONE 1 - Step 1.3.3: Encode Categorical Variables
======================================================
Task 3: Preprocessing and Feature Engineering

Encode categorical variables for machine learning:
- Store Type (A, B, C) → One-Hot Encoding

"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.3.3: ENCODE CATEGORICAL VARIABLES")
print("="*80)

print("\n[1] Loading data with lag features...")
train = pd.read_csv('processed_data/Stage1.3.2/train_lag_features.csv')
test = pd.read_csv('processed_data/Stage1.3.2/test_lag_features.csv')
print(f"Loaded: train {train.shape}, test {test.shape}")

print("\n[2] One-hot encoding Store Type...")
train_encoded = pd.get_dummies(train, columns=['Type'], prefix='Type', drop_first=False)
test_encoded = pd.get_dummies(test, columns=['Type'], prefix='Type', drop_first=False)
type_columns = [col for col in train_encoded.columns if col.startswith('Type_')]
print(f"Encoded Type column to: {type_columns}")

print("\n[3] Saving encoded data...")
output_dir = 'processed_data/Stage1.3.3'
os.makedirs(output_dir, exist_ok=True)
train_output = os.path.join(output_dir, 'train_encoded.csv')
test_output = os.path.join(output_dir, 'test_encoded.csv')
train_encoded.to_csv(train_output, index=False)
test_encoded.to_csv(test_output, index=False)
print(f"Saved: {train_output}, {test_output}")

print("\n" + "="*80)
print("STEP 1.3.3 COMPLETED!")
print("="*80)
