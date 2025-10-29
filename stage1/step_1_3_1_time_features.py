"""
MILESTONE 1 - Step 1.3.1: Create Time-Based Features
====================================================
Task 3: Preprocessing and Feature Engineering

Create time-based features from Date column:
- Month, Week, Day, Quarter, DayOfWeek, WeekOfYear
- Is_Weekend, Is_Month_Start, Is_Month_End
- Year (for trend analysis)

"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.3.1: CREATE TIME-BASED FEATURES")
print("="*80)

print("\n[1] Loading cleaned data...")
train = pd.read_csv('processed_data/Stage1.2/train_cleaned_step2.csv')
test = pd.read_csv('processed_data/Stage1.2/test_cleaned_step2.csv')
train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])
print(f"Loaded: train {train.shape}, test {test.shape}")

def create_time_features(df, dataset_name):
    """Create time-based features from Date column"""
    # Basic time components
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Quarter'] = df['Date'].dt.quarter
    df['DayOfWeek'] = df['Date'].dt.dayofweek
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week
    
    # Binary indicators
    df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)
    df['Is_Month_Start'] = df['Date'].dt.is_month_start.astype(int)
    df['Is_Month_End'] = df['Date'].dt.is_month_end.astype(int)
    df['Is_Quarter_Start'] = df['Date'].dt.is_quarter_start.astype(int)
    df['Is_Quarter_End'] = df['Date'].dt.is_quarter_end.astype(int)
    df['Is_Year_Start'] = df['Date'].dt.is_year_start.astype(int)
    df['Is_Year_End'] = df['Date'].dt.is_year_end.astype(int)
    
    # Cyclical features
    df['Month_Sin'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['Month_Cos'] = np.cos(2 * np.pi * df['Month'] / 12)
    df['Week_Sin'] = np.sin(2 * np.pi * df['WeekOfYear'] / 52)
    df['Week_Cos'] = np.cos(2 * np.pi * df['WeekOfYear'] / 52)
    df['DayOfWeek_Sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
    df['DayOfWeek_Cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)
    
    return df

print("\n[2] Creating time-based features...")
train = create_time_features(train, "Training Data")
test = create_time_features(test, "Test Data")
print("Created 20 time-based features")

print("\n[3] Saving data with time features...")
output_dir = 'processed_data/Stage1.3.1'
os.makedirs(output_dir, exist_ok=True)
train_output = os.path.join(output_dir, 'train_time_features.csv')
test_output = os.path.join(output_dir, 'test_time_features.csv')
train.to_csv(train_output, index=False)
test.to_csv(test_output, index=False)
print(f"Saved: {train_output}, {test_output}")

print("\n" + "="*80)
print("STEP 1.3.1 COMPLETED!")
print("="*80)

