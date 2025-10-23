"""
Feature Engineering Pipeline - Steps 1.3.1 through 1.3.4
=========================================================
This script applies all feature engineering steps sequentially:
- Step 1.3.1: Time-based features
- Step 1.3.2: Lag features
- Step 1.3.3: Categorical encoding
- Step 1.3.4: Numerical normalization

Input: processed_data/Stage1.2/train_cleaned_step2.csv & test_cleaned_step2.csv
Output: processed_data/Final/train_final.csv & test_final.csv
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

print("="*80)
print("🚀 FEATURE ENGINEERING PIPELINE")
print("="*80)
print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# STEP 0: Load Data from Stage 1.2
# ============================================================================
print("\n" + "="*80)
print("📥 STEP 0: LOADING DATA FROM STAGE 1.2")
print("="*80)

train = pd.read_csv('processed_data/Stage1.2/train_cleaned_step2.csv')
test = pd.read_csv('processed_data/Stage1.2/test_cleaned_step2.csv')

# Convert Date to datetime
train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])

print(f"✅ Training Data Loaded: {train.shape}")
print(f"✅ Test Data Loaded: {test.shape}")
print(f"\n📋 Initial Columns ({len(train.columns)}): {list(train.columns)}")

# ============================================================================
# STEP 1.3.1: Create Time-Based Features
# ============================================================================
print("\n" + "="*80)
print("⏰ STEP 1.3.1: CREATING TIME-BASED FEATURES")
print("="*80)

# Basic time features - Train
train['Year'] = train['Date'].dt.year
train['Month'] = train['Date'].dt.month
train['Day'] = train['Date'].dt.day
train['Quarter'] = train['Date'].dt.quarter
train['DayOfWeek'] = train['Date'].dt.dayofweek
train['WeekOfYear'] = train['Date'].dt.isocalendar().week.astype(int)

# Basic time features - Test
test['Year'] = test['Date'].dt.year
test['Month'] = test['Date'].dt.month
test['Day'] = test['Date'].dt.day
test['Quarter'] = test['Date'].dt.quarter
test['DayOfWeek'] = test['Date'].dt.dayofweek
test['WeekOfYear'] = test['Date'].dt.isocalendar().week.astype(int)

# Binary time indicators - Train
train['Is_Weekend'] = (train['DayOfWeek'] >= 5).astype(int)
train['Is_Month_Start'] = train['Date'].dt.is_month_start.astype(int)
train['Is_Month_End'] = train['Date'].dt.is_month_end.astype(int)
train['Is_Quarter_Start'] = train['Date'].dt.is_quarter_start.astype(int)
train['Is_Quarter_End'] = train['Date'].dt.is_quarter_end.astype(int)
train['Is_Year_Start'] = train['Date'].dt.is_year_start.astype(int)
train['Is_Year_End'] = train['Date'].dt.is_year_end.astype(int)

# Binary time indicators - Test
test['Is_Weekend'] = (test['DayOfWeek'] >= 5).astype(int)
test['Is_Month_Start'] = test['Date'].dt.is_month_start.astype(int)
test['Is_Month_End'] = test['Date'].dt.is_month_end.astype(int)
test['Is_Quarter_Start'] = test['Date'].dt.is_quarter_start.astype(int)
test['Is_Quarter_End'] = test['Date'].dt.is_quarter_end.astype(int)
test['Is_Year_Start'] = test['Date'].dt.is_year_start.astype(int)
test['Is_Year_End'] = test['Date'].dt.is_year_end.astype(int)

# Cyclical encoding - Train
train['Month_Sin'] = np.sin(2 * np.pi * train['Month'] / 12)
train['Month_Cos'] = np.cos(2 * np.pi * train['Month'] / 12)
train['Week_Sin'] = np.sin(2 * np.pi * train['WeekOfYear'] / 52)
train['Week_Cos'] = np.cos(2 * np.pi * train['WeekOfYear'] / 52)
train['DayOfWeek_Sin'] = np.sin(2 * np.pi * train['DayOfWeek'] / 7)
train['DayOfWeek_Cos'] = np.cos(2 * np.pi * train['DayOfWeek'] / 7)

# Cyclical encoding - Test
test['Month_Sin'] = np.sin(2 * np.pi * test['Month'] / 12)
test['Month_Cos'] = np.cos(2 * np.pi * test['Month'] / 12)
test['Week_Sin'] = np.sin(2 * np.pi * test['WeekOfYear'] / 52)
test['Week_Cos'] = np.cos(2 * np.pi * test['WeekOfYear'] / 52)
test['DayOfWeek_Sin'] = np.sin(2 * np.pi * test['DayOfWeek'] / 7)
test['DayOfWeek_Cos'] = np.cos(2 * np.pi * test['DayOfWeek'] / 7)

time_features = ['Year', 'Month', 'Day', 'Quarter', 'DayOfWeek', 'WeekOfYear',
                'Is_Weekend', 'Is_Month_Start', 'Is_Month_End', 'Is_Quarter_Start',
                'Is_Quarter_End', 'Is_Year_Start', 'Is_Year_End',
                'Month_Sin', 'Month_Cos', 'Week_Sin', 'Week_Cos',
                'DayOfWeek_Sin', 'DayOfWeek_Cos']

print(f"✅ Created {len(time_features)} time-based features:")
for i, feat in enumerate(time_features, 1):
    print(f"   {i:2d}. {feat}")

print(f"\n📊 Current shape - Train: {train.shape}, Test: {test.shape}")

# Save Step 1.3.1 output
print("\n💾 Saving Step 1.3.1 output...")
os.makedirs('processed_data/Stage1.3.1', exist_ok=True)
train.to_csv('processed_data/Stage1.3.1/train_time_features.csv', index=False)
test.to_csv('processed_data/Stage1.3.1/test_time_features.csv', index=False)
print(f"✅ Saved: processed_data/Stage1.3.1/train_time_features.csv")
print(f"✅ Saved: processed_data/Stage1.3.1/test_time_features.csv")

# ============================================================================
# STEP 1.3.2: Create Lag Features
# ============================================================================
print("\n" + "="*80)
print("📊 STEP 1.3.2: CREATING LAG FEATURES")
print("="*80)

# Sort data for lag feature creation
train = train.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

# Create lag features for training data
print("Creating lag features for training data...")
train['Sales_Lag1'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(1)
train['Sales_Lag2'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(2)
train['Sales_Lag4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(4)

# Rolling statistics
print("Creating rolling statistics...")
train['Sales_Rolling_Mean_4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).mean()
)
train['Sales_Rolling_Mean_8'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=8, min_periods=1).mean()
)
train['Sales_Rolling_Std_4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).std()
)

# Sales momentum
print("Creating momentum feature...")
train['Sales_Momentum'] = train['Sales_Lag1'] - train['Sales_Lag2']

# Fill NaN values
lag_cols = ['Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4', 
           'Sales_Rolling_Mean_4', 'Sales_Rolling_Mean_8', 
           'Sales_Rolling_Std_4', 'Sales_Momentum']
for col in lag_cols:
    train[col] = train[col].fillna(0)

# For test data, initialize lag features to 0
print("Initializing lag features for test data...")
for col in lag_cols:
    test[col] = 0

print(f"✅ Created {len(lag_cols)} lag features:")
for i, feat in enumerate(lag_cols, 1):
    print(f"   {i}. {feat}")

print(f"\n⚠️  Note: Test dataset lag features initialized to 0 (no historical sales)")
print(f"📊 Current shape - Train: {train.shape}, Test: {test.shape}")

# Save Step 1.3.2 output
print("\n💾 Saving Step 1.3.2 output...")
os.makedirs('processed_data/Stage1.3.2', exist_ok=True)
train.to_csv('processed_data/Stage1.3.2/train_lag_features.csv', index=False)
test.to_csv('processed_data/Stage1.3.2/test_lag_features.csv', index=False)
print(f"✅ Saved: processed_data/Stage1.3.2/train_lag_features.csv")
print(f"✅ Saved: processed_data/Stage1.3.2/test_lag_features.csv")

# ============================================================================
# STEP 1.3.3: Encode Categorical Variables
# ============================================================================
print("\n" + "="*80)
print("🔤 STEP 1.3.3: ENCODING CATEGORICAL VARIABLES")
print("="*80)

# Manual one-hot encoding (more memory efficient for large datasets)
print("Applying One-Hot Encoding to 'Type' column...")

train['Type_A'] = (train['Type'] == 'A').astype(int)
train['Type_B'] = (train['Type'] == 'B').astype(int)
train['Type_C'] = (train['Type'] == 'C').astype(int)

test['Type_A'] = (test['Type'] == 'A').astype(int)
test['Type_B'] = (test['Type'] == 'B').astype(int)
test['Type_C'] = (test['Type'] == 'C').astype(int)

# Drop original Type column
train = train.drop('Type', axis=1)
test = test.drop('Type', axis=1)

categorical_features = ['Type_A', 'Type_B', 'Type_C']

print(f"✅ Encoded categorical variables:")
print(f"   • Type → Type_A, Type_B, Type_C")
print(f"\n📊 Current shape - Train: {train.shape}, Test: {test.shape}")

# Save Step 1.3.3 output
print("\n💾 Saving Step 1.3.3 output...")
os.makedirs('processed_data/Stage1.3.3', exist_ok=True)
train.to_csv('processed_data/Stage1.3.3/train_encoded.csv', index=False)
test.to_csv('processed_data/Stage1.3.3/test_encoded.csv', index=False)
print(f"✅ Saved: processed_data/Stage1.3.3/train_encoded.csv")
print(f"✅ Saved: processed_data/Stage1.3.3/test_encoded.csv")

# ============================================================================
# STEP 1.3.4: Normalize Numerical Features
# ============================================================================
print("\n" + "="*80)
print("📐 STEP 1.3.4: NORMALIZING NUMERICAL FEATURES")
print("="*80)

# Define continuous features to normalize
continuous_features = [
    'Size', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment',
    'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5',
    'Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4',
    'Sales_Rolling_Mean_4', 'Sales_Rolling_Mean_8', 'Sales_Rolling_Std_4',
    'Sales_Momentum'
]

print(f"Applying Z-score normalization to {len(continuous_features)} features...")
print("Method: (X - mean) / std")

# Calculate normalization parameters from training data
norm_params = {}
for feature in continuous_features:
    mean = train[feature].mean()
    std = train[feature].std()
    
    # Store parameters
    norm_params[feature] = {
        'mean': float(mean),
        'std': float(std)
    }
    
    # Apply normalization (avoid division by zero)
    if std != 0:
        train[feature] = (train[feature] - mean) / std
        test[feature] = (test[feature] - mean) / std
    else:
        train[feature] = 0
        test[feature] = 0
    
    print(f"   ✓ {feature:25s} (μ={mean:10.2f}, σ={std:10.2f})")

print(f"\n✅ Normalization complete!")
print(f"📊 Final shape - Train: {train.shape}, Test: {test.shape}")

# ============================================================================
# SAVE FINAL DATASETS
# ============================================================================
print("\n" + "="*80)
print("💾 SAVING FINAL DATASETS")
print("="*80)

# Create output directory
os.makedirs('processed_data/Final', exist_ok=True)

# Save datasets
train.to_csv('processed_data/Final/train_final.csv', index=False)
test.to_csv('processed_data/Final/test_final.csv', index=False)

# Save normalization parameters
with open('processed_data/Final/normalization_params.json', 'w') as f:
    json.dump(norm_params, f, indent=2)

print(f"✅ Saved: processed_data/Final/train_final.csv")
print(f"✅ Saved: processed_data/Final/test_final.csv")
print(f"✅ Saved: processed_data/Final/normalization_params.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*80)
print("📊 FEATURE ENGINEERING PIPELINE - SUMMARY")
print("="*80)

print(f"\n📥 INPUT:")
print(f"   • Train: processed_data/Stage1.2/train_cleaned_step2.csv")
print(f"   • Test:  processed_data/Stage1.2/test_cleaned_step2.csv")

print(f"\n🔧 TRANSFORMATIONS APPLIED:")
print(f"   1. Time-based features:     {len(time_features)} features")
print(f"   2. Lag features:            {len(lag_cols)} features")
print(f"   3. Categorical encoding:    {len(categorical_features)} features")
print(f"   4. Numerical normalization: {len(continuous_features)} features")

print(f"\n📤 OUTPUT:")
print(f"\n   Step 1.3.1 - Time Features:")
print(f"   • processed_data/Stage1.3.1/train_time_features.csv (40 cols)")
print(f"   • processed_data/Stage1.3.1/test_time_features.csv (39 cols)")
print(f"\n   Step 1.3.2 - Lag Features:")
print(f"   • processed_data/Stage1.3.2/train_lag_features.csv (47 cols)")
print(f"   • processed_data/Stage1.3.2/test_lag_features.csv (46 cols)")
print(f"\n   Step 1.3.3 - Encoded:")
print(f"   • processed_data/Stage1.3.3/train_encoded.csv (49 cols)")
print(f"   • processed_data/Stage1.3.3/test_encoded.csv (48 cols)")
print(f"\n   Step 1.3.4 - Final Normalized:")
print(f"   • processed_data/Final/train_final.csv ({train.shape[0]} rows × {train.shape[1]} cols)")
print(f"   • processed_data/Final/test_final.csv ({test.shape[0]} rows × {test.shape[1]} cols)")
print(f"   • processed_data/Final/normalization_params.json")

print(f"\n📋 FINAL FEATURE SET ({train.shape[1]} columns):")
original_cols = ['Store', 'Dept', 'Date', 'IsHoliday', 'Size', 'Temperature', 
                'Fuel_Price', 'CPI', 'Unemployment', 
                'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5',
                'Has_MarkDown1', 'Has_MarkDown2', 'Has_MarkDown3', 'Has_MarkDown4', 'Has_MarkDown5']
print(f"   • Original features: {len([c for c in original_cols if c in train.columns])}")
print(f"   • Time features: {len(time_features)}")
print(f"   • Lag features: {len(lag_cols)}")
print(f"   • Encoded features: {len(categorical_features)}")
if 'Weekly_Sales' in train.columns:
    print(f"   • Target variable: Weekly_Sales")

print(f"\n✅ Data Quality Checks:")
print(f"   • Train missing values: {train.isnull().sum().sum()}")
print(f"   • Test missing values: {test.isnull().sum().sum()}")
print(f"   • Train duplicates: {train.duplicated().sum()}")
print(f"   • Test duplicates: {test.duplicated().sum()}")

print(f"\n⏱️  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
print("🎉 FEATURE ENGINEERING PIPELINE COMPLETE!")
print("="*80)
print("\n🚀 Ready for Model Development (Milestone 2)!")
