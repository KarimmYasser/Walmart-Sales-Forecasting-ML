"""
MILESTONE 1 - Step 1.1: Data Loading & Merging
================================================
This script loads all Walmart datasets and merges them into a unified dataset.

Author: Data Science Team
Date: October 23, 2025
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

print("\n[1] Loading Individual Datasets...")
print("-" * 80)

# Load training data
print("\n📊 Loading Training Data (train.csv)...")
train = pd.read_csv(TRAIN_PATH)
print(f"   ✓ Shape: {train.shape}")
print(f"   ✓ Date Range: {train['Date'].min()} to {train['Date'].max()}")
print(f"   ✓ Columns: {list(train.columns)}")
print(f"   ✓ Stores: {train['Store'].nunique()} unique stores")
print(f"   ✓ Departments: {train['Dept'].nunique()} unique departments")
print(f"   ✓ Missing Values: {train.isnull().sum().sum()} total")

# Load test data
print("\n📊 Loading Test Data (test.csv)...")
test = pd.read_csv(TEST_PATH)
print(f"   ✓ Shape: {test.shape}")
print(f"   ✓ Date Range: {test['Date'].min()} to {test['Date'].max()}")
print(f"   ✓ Columns: {list(test.columns)}")
print(f"   ✓ Missing Values: {test.isnull().sum().sum()} total")

# Load stores data
print("\n🏪 Loading Stores Data (stores.csv)...")
stores = pd.read_csv(STORES_PATH)
print(f"   ✓ Shape: {stores.shape}")
print(f"   ✓ Columns: {list(stores.columns)}")
print(f"   ✓ Store Types Distribution:")
for store_type in stores['Type'].unique():
    count = (stores['Type'] == store_type).sum()
    print(f"      - Type {store_type}: {count} stores")
print(f"   ✓ Missing Values: {stores.isnull().sum().sum()} total")

# Load features data
print("\n📈 Loading Features Data (features.xlsx)...")
features = pd.read_excel(FEATURES_PATH)
print(f"   ✓ Shape: {features.shape}")
print(f"   ✓ Columns: {list(features.columns)}")
print(f"   ✓ Missing Values:")
for col in features.columns:
    null_count = features[col].isnull().sum()
    if null_count > 0:
        null_pct = (null_count / len(features)) * 100
        print(f"      - {col}: {null_count} ({null_pct:.1f}%)")

print("\n" + "="*80)
print("[2] Data Validation & Quality Checks")
print("="*80)

# Check for duplicate rows
print("\n🔍 Checking for Duplicates...")
train_dupes = train.duplicated(subset=['Store', 'Dept', 'Date']).sum()
features_dupes = features.duplicated(subset=['Store', 'Date']).sum()
print(f"   ✓ Train duplicates (Store-Dept-Date): {train_dupes}")
print(f"   ✓ Features duplicates (Store-Date): {features_dupes}")

# Check for negative sales
print("\n💰 Checking Sales Data...")
negative_sales = (train['Weekly_Sales'] < 0).sum()
print(f"   ✓ Negative sales entries: {negative_sales}")
if negative_sales > 0:
    print(f"   ⚠ Warning: Found {negative_sales} negative sales values")
    print(f"      Min Sales: ${train['Weekly_Sales'].min():,.2f}")
    print(f"      These may represent returns/clearances")

# Basic statistics
print(f"   ✓ Sales Statistics:")
print(f"      - Mean: ${train['Weekly_Sales'].mean():,.2f}")
print(f"      - Median: ${train['Weekly_Sales'].median():,.2f}")
print(f"      - Std Dev: ${train['Weekly_Sales'].std():,.2f}")
print(f"      - Max: ${train['Weekly_Sales'].max():,.2f}")

print("\n" + "="*80)
print("[3] Merging Datasets")
print("="*80)

# Step 1: Merge train with stores
print("\n🔗 Step 3.1: Merging Train + Stores...")
print(f"   Before merge: Train shape = {train.shape}")
train_full = train.merge(stores, on='Store', how='left')
print(f"   After merge:  Train shape = {train_full.shape}")
print(f"   ✓ Added columns: {[col for col in train_full.columns if col not in train.columns]}")

# Check merge quality
null_type = train_full['Type'].isnull().sum()
null_size = train_full['Size'].isnull().sum()
if null_type > 0 or null_size > 0:
    print(f"   ⚠ Warning: Found {null_type} null Type values and {null_size} null Size values")
else:
    print(f"   ✓ Merge successful - no null values in store attributes")

# Step 2: Merge with features
print("\n🔗 Step 3.2: Merging Train+Stores + Features...")
print(f"   Before merge: Train shape = {train_full.shape}")

# Convert dates to datetime for proper merging
train_full['Date'] = pd.to_datetime(train_full['Date'])
features['Date'] = pd.to_datetime(features['Date'])

train_full = train_full.merge(features, on=['Store', 'Date', 'IsHoliday'], how='left')
print(f"   After merge:  Train shape = {train_full.shape}")
print(f"   ✓ Added feature columns: {[col for col in train_full.columns if col in features.columns and col not in ['Store', 'Date', 'IsHoliday']]}")

# Step 3: Create test dataset with same structure
print("\n🔗 Step 3.3: Preparing Test Dataset...")
test['Date'] = pd.to_datetime(test['Date'])
test_full = test.merge(stores, on='Store', how='left')
test_full = test_full.merge(features, on=['Store', 'Date', 'IsHoliday'], how='left')
print(f"   ✓ Test dataset shape: {test_full.shape}")
print(f"   ✓ Test columns: {len(test_full.columns)} (same as train minus Weekly_Sales)")

print("\n" + "="*80)
print("[4] Final Dataset Summary")
print("="*80)

print("\n📋 Training Dataset (train_full):")
print(f"   Shape: {train_full.shape}")
print(f"   Date Range: {train_full['Date'].min()} to {train_full['Date'].max()}")
print(f"   Total Records: {len(train_full):,}")
print(f"   Columns: {len(train_full.columns)}")

print("\n📋 Column List:")
for i, col in enumerate(train_full.columns, 1):
    null_count = train_full[col].isnull().sum()
    null_pct = (null_count / len(train_full)) * 100
    dtype = train_full[col].dtype
    print(f"   {i:2d}. {col:20s} | Type: {str(dtype):15s} | Nulls: {null_count:6d} ({null_pct:5.1f}%)")

print("\n📋 Test Dataset (test_full):")
print(f"   Shape: {test_full.shape}")
print(f"   Date Range: {test_full['Date'].min()} to {test_full['Date'].max()}")
print(f"   Total Records: {len(test_full):,}")

print("\n" + "="*80)
print("[5] Saving Merged Datasets")
print("="*80)

# Create output directory if it doesn't exist
output_dir = 'processed_data'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"\n✓ Created directory: {output_dir}/")

# Save merged datasets
train_output = os.path.join(output_dir, 'train_merged.csv')
test_output = os.path.join(output_dir, 'test_merged.csv')

print(f"\n💾 Saving merged datasets...")
train_full.to_csv(train_output, index=False)
print(f"   ✓ Saved: {train_output} ({os.path.getsize(train_output) / 1024 / 1024:.2f} MB)")

test_full.to_csv(test_output, index=False)
print(f"   ✓ Saved: {test_output} ({os.path.getsize(test_output) / 1024 / 1024:.2f} MB)")

print("\n" + "="*80)
print("[6] Quick Data Preview")
print("="*80)

print("\n📊 First 5 rows of merged training data:")
print(train_full.head())

print("\n📊 Sample of data for one store-department combination:")
sample = train_full[(train_full['Store'] == 1) & (train_full['Dept'] == 1)].head(10)
print(sample[['Store', 'Dept', 'Date', 'Weekly_Sales', 'Type', 'Size', 'Temperature', 'IsHoliday']])

print("\n" + "="*80)
print("✅ STEP 1.1 COMPLETED SUCCESSFULLY!")
print("="*80)
print(f"\n📁 Output Files:")
print(f"   - {train_output}")
print(f"   - {test_output}")
print(f"\n📊 Dataset Statistics:")
print(f"   - Training records: {len(train_full):,}")
print(f"   - Test records: {len(test_full):,}")
print(f"   - Features per record: {len(train_full.columns)}")
print(f"   - Ready for Step 1.2: Handling Missing Values")
print("\n" + "="*80)

