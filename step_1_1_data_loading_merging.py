"""
MILESTONE 1 - Step 1.1: Data Loading & Merging
================================================
This script loads all Walmart datasets and merges them into a unified dataset.

"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.1: DATA LOADING & MERGING")
print("="*80)

# Define file paths
BASE_PATH = 'datasets/walmart-recruiting-store-sales-forecasting/'
TRAIN_PATH = os.path.join(BASE_PATH, 'train.csv')
TEST_PATH = os.path.join(BASE_PATH, 'test.csv')
STORES_PATH = os.path.join(BASE_PATH, 'stores.csv')
FEATURES_PATH = os.path.join(BASE_PATH, 'features.xlsx')

print("\n[1] Loading datasets...")
train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)
stores = pd.read_csv(STORES_PATH)
features = pd.read_excel(FEATURES_PATH)
print(f"✓ Loaded: train {train.shape}, test {test.shape}, stores {stores.shape}, features {features.shape}")

print("\n[2] Merging datasets...")
train_full = train.merge(stores, on='Store', how='left')
train_full['Date'] = pd.to_datetime(train_full['Date'])
features['Date'] = pd.to_datetime(features['Date'])
train_full = train_full.merge(features, on=['Store', 'Date', 'IsHoliday'], how='left')

test['Date'] = pd.to_datetime(test['Date'])
test_full = test.merge(stores, on='Store', how='left')
test_full = test_full.merge(features, on=['Store', 'Date', 'IsHoliday'], how='left')
print(f"✓ Merged: train_full {train_full.shape}, test_full {test_full.shape}")

print("\n[3] Saving merged datasets...")
output_dir = 'processed_data'
os.makedirs(output_dir, exist_ok=True)
train_output = os.path.join(output_dir, 'train_merged.csv')
test_output = os.path.join(output_dir, 'test_merged.csv')
train_full.to_csv(train_output, index=False)
test_full.to_csv(test_output, index=False)
print(f"✓ Saved: {train_output}, {test_output}")

print("\n" + "="*80)
print("✅ STEP 1.1 COMPLETED!")
print("="*80)

