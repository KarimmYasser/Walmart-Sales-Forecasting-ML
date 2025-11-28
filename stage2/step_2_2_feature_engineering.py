"""
============================================================================
Milestone 2 - Task 2.2: Enhanced Feature Engineering
============================================================================
This script creates advanced features beyond Milestone 1:
1. Advanced Rolling Statistics (multiple windows, exponential moving averages)
2. Seasonal Decomposition Features
3. Holiday Proximity Features
4. Store Performance Rankings
5. Department Interaction Features
6. Promotional Intensity Metrics
7. Economic Indicator Interactions

Input: processed_data/Final/train_final.csv, test_final.csv
Output: outputs/enhanced_features/
============================================================================
"""

import pandas as pd
import numpy as np
import json
import os

print("MILESTONE 2 - TASK 2.2: ENHANCED FEATURE ENGINEERING")

# Determine correct path to Stage 1 output
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
stage1_output = os.path.join(project_root, 'stage1', 'processed_data', 'Stage1.3.4_Final')

# Load and prepare data
train = pd.read_csv(os.path.join(stage1_output, 'train_final.csv'))
test = pd.read_csv(os.path.join(stage1_output, 'test_final.csv'))
train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])
train = train.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)
test = test.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

# Advanced Rolling Statistics
print("\n[1/6] Creating advanced rolling features...")

def create_advanced_rolling_features(df, has_sales=True):
    """Create advanced rolling window features"""
    df_copy = df.copy()
    
    if has_sales:
        # Exponential Moving Averages
        df_copy['Sales_EMA_4'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.ewm(span=4, adjust=False).mean())
        df_copy['Sales_EMA_8'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.ewm(span=8, adjust=False).mean())
        df_copy['Sales_EMA_12'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.ewm(span=12, adjust=False).mean())
        
        # Rolling Min/Max
        df_copy['Sales_Rolling_Min_4'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).min())
        df_copy['Sales_Rolling_Max_4'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).max())
        df_copy['Sales_Rolling_Range_4'] = df_copy['Sales_Rolling_Max_4'] - df_copy['Sales_Rolling_Min_4']
        df_copy['Sales_Trend'] = df_copy['Sales_EMA_4'] - df_copy['Sales_EMA_12']
        
        # Coefficient of Variation
        rolling_mean = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).mean())
        rolling_std = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).std())
        df_copy['Sales_CV_4'] = rolling_std / (rolling_mean + 1)
        df_copy['Sales_Acceleration'] = df_copy.groupby(['Store', 'Dept'])['Sales_Momentum'].transform(
            lambda x: x.diff())
    
    return df_copy

train = create_advanced_rolling_features(train, has_sales=True)
test = create_advanced_rolling_features(test, has_sales=False)

# Seasonal Features
print("[2/6] Creating seasonal features...")

def create_seasonal_features(df):
    """Create seasonal and holiday-related features"""
    df_copy = df.copy()
    df_copy['Season'] = df_copy['Month'].apply(lambda x: 
        'Winter' if x in [12, 1, 2] else 'Spring' if x in [3, 4, 5] else
        'Summer' if x in [6, 7, 8] else 'Fall')
    df_copy['Is_Holiday_Season'] = ((df_copy['Month'] == 11) | (df_copy['Month'] == 12)).astype(int)
    df_copy['Is_BackToSchool_Season'] = ((df_copy['Month'] == 7) | (df_copy['Month'] == 8)).astype(int)
    df_copy['Is_SuperBowl_Week'] = ((df_copy['Month'] == 2) & (df_copy['Day'] <= 14)).astype(int)
    df_copy['Days_To_Thanksgiving'] = df_copy.apply(lambda row: 
        (pd.Timestamp(f"{row['Year']}-11-24") - row['Date']).days if row['Month'] <= 11 
        else (pd.Timestamp(f"{row['Year']+1}-11-24") - row['Date']).days, axis=1)
    df_copy['Days_To_Christmas'] = df_copy.apply(lambda row: 
        (pd.Timestamp(f"{row['Year']}-12-25") - row['Date']).days if row['Month'] <= 12 
        else (pd.Timestamp(f"{row['Year']+1}-12-25") - row['Date']).days, axis=1)
    df_copy['Season_Winter'] = (df_copy['Season'] == 'Winter').astype(int)
    df_copy['Season_Spring'] = (df_copy['Season'] == 'Spring').astype(int)
    df_copy['Season_Summer'] = (df_copy['Season'] == 'Summer').astype(int)
    df_copy['Season_Fall'] = (df_copy['Season'] == 'Fall').astype(int)
    df_copy = df_copy.drop('Season', axis=1)
    return df_copy

train = create_seasonal_features(train)
test = create_seasonal_features(test)

# Store Performance Features
print("[3/6] Creating store performance features...")

store_stats = train.groupby('Store')['Weekly_Sales'].agg([
    ('Store_Avg_Sales', 'mean'), ('Store_Std_Sales', 'std'),
    ('Store_Min_Sales', 'min'), ('Store_Max_Sales', 'max')]).reset_index()
dept_stats = train.groupby('Dept')['Weekly_Sales'].agg([
    ('Dept_Avg_Sales', 'mean'), ('Dept_Std_Sales', 'std')]).reset_index()
store_dept_stats = train.groupby(['Store', 'Dept'])['Weekly_Sales'].agg([
    ('StoreDept_Avg_Sales', 'mean'), ('StoreDept_Std_Sales', 'std')]).reset_index()

train = train.merge(store_stats, on='Store', how='left')
train = train.merge(dept_stats, on='Dept', how='left')
train = train.merge(store_dept_stats, on=['Store', 'Dept'], how='left')
test = test.merge(store_stats, on='Store', how='left')
test = test.merge(dept_stats, on='Dept', how='left')
test = test.merge(store_dept_stats, on=['Store', 'Dept'], how='left')

if 'Weekly_Sales' in train.columns:
    train['Sales_Deviation_From_Store_Avg'] = train['Weekly_Sales'] - train['Store_Avg_Sales']
    train['Sales_Deviation_From_Dept_Avg'] = train['Weekly_Sales'] - train['Dept_Avg_Sales']
    train['Sales_Deviation_From_StoreDept_Avg'] = train['Weekly_Sales'] - train['StoreDept_Avg_Sales']

# Promotional Intensity Metrics
print("[4/6] Creating promotional features...")

def create_promo_features(df):
    df_copy = df.copy()
    markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    df_copy['Total_MarkDown'] = df_copy[markdown_cols].sum(axis=1)
    has_markdown_cols = [f'Has_{col}' for col in markdown_cols]
    if all(col in df_copy.columns for col in has_markdown_cols):
        df_copy['Num_Active_MarkDowns'] = df_copy[has_markdown_cols].sum(axis=1)
    df_copy['Promo_Intensity'] = df_copy['Total_MarkDown'] / (df_copy['Size'] + 1)
    df_copy['Total_MarkDown_Rolling_4'] = df_copy.groupby(['Store', 'Dept'])['Total_MarkDown'].transform(
        lambda x: x.rolling(window=4, min_periods=1).mean())
    return df_copy

train = create_promo_features(train)
test = create_promo_features(test)

# Economic Indicator Interactions
print("[5/6] Creating economic interactions...")

def create_economic_interactions(df):
    df_copy = df.copy()
    df_copy['Economic_Stress'] = df_copy['CPI'] * df_copy['Unemployment']
    df_copy['Holiday_Temperature'] = df_copy['Temperature'] * df_copy['IsHoliday']
    df_copy['Spending_Power'] = df_copy['Fuel_Price'] * df_copy['Unemployment']
    df_copy['Store_Purchasing_Power'] = df_copy['Size'] * df_copy['CPI']
    return df_copy

train = create_economic_interactions(train)
test = create_economic_interactions(test)

# Time-Based Aggregations
print("[6/6] Creating time aggregations...")

def create_time_aggregations(df, has_sales=True):
    df_copy = df.copy()
    if has_sales:
        df_copy['Month_Store_Avg_Sales'] = df_copy.groupby(['Store', 'Year', 'Month'])['Weekly_Sales'].transform('mean')
        df_copy['Month_Store_Total_Sales'] = df_copy.groupby(['Store', 'Year', 'Month'])['Weekly_Sales'].transform('sum')
        df_copy['Quarter_Store_Avg_Sales'] = df_copy.groupby(['Store', 'Year', 'Quarter'])['Weekly_Sales'].transform('mean')
        df_copy['Quarter_Store_Total_Sales'] = df_copy.groupby(['Store', 'Year', 'Quarter'])['Weekly_Sales'].transform('sum')
        df_copy['Store_Sales_YoY_Growth'] = df_copy.groupby(['Store', 'Month', 'Day'])['Weekly_Sales'].transform(
            lambda x: x.pct_change(periods=1))
    return df_copy

train = create_time_aggregations(train, has_sales=True)
test = create_time_aggregations(test, has_sales=False)

# Save Enhanced Datasets
output_dir = os.path.join(script_dir, 'outputs', 'enhanced_features')
os.makedirs(output_dir, exist_ok=True)
train.to_csv(os.path.join(output_dir, 'train_enhanced.csv'), index=False)
test.to_csv(os.path.join(output_dir, 'test_enhanced.csv'), index=False)

# Create feature summary
new_features = {
    'advanced_rolling': [
        'Sales_EMA_4', 'Sales_EMA_8', 'Sales_EMA_12',
        'Sales_Rolling_Min_4', 'Sales_Rolling_Max_4', 'Sales_Rolling_Range_4',
        'Sales_Trend', 'Sales_CV_4', 'Sales_Acceleration'
    ],
    'seasonal': [
        'Is_Holiday_Season', 'Is_BackToSchool_Season', 'Is_SuperBowl_Week',
        'Days_To_Thanksgiving', 'Days_To_Christmas',
        'Season_Winter', 'Season_Spring', 'Season_Summer', 'Season_Fall'
    ],
    'store_performance': [
        'Store_Avg_Sales', 'Store_Std_Sales', 'Store_Min_Sales', 'Store_Max_Sales',
        'Dept_Avg_Sales', 'Dept_Std_Sales', 'StoreDept_Avg_Sales', 'StoreDept_Std_Sales',
        'Sales_Deviation_From_Store_Avg', 'Sales_Deviation_From_Dept_Avg', 
        'Sales_Deviation_From_StoreDept_Avg'
    ],
    'promotional': [
        'Total_MarkDown', 'Num_Active_MarkDowns', 'Promo_Intensity',
        'Total_MarkDown_Rolling_4'
    ],
    'economic_interactions': [
        'Economic_Stress', 'Holiday_Temperature', 'Spending_Power',
        'Store_Purchasing_Power'
    ],
    'time_aggregations': [
        'Month_Store_Avg_Sales', 'Month_Store_Total_Sales',
        'Quarter_Store_Avg_Sales', 'Quarter_Store_Total_Sales',
        'Store_Sales_YoY_Growth'
    ]
}

# Save feature summary
feature_summary = {
    'total_new_features': sum(len(v) for v in new_features.values()),
    'feature_categories': new_features,
    'train_shape': train.shape,
    'test_shape': test.shape,
    'original_features': 49,  # From Milestone 1
    'total_features_now': train.shape[1]
}

with open(os.path.join(output_dir, 'feature_summary.json'), 'w') as f:
    json.dump(feature_summary, f, indent=4, default=str)

print(f"\nTASK 2.2 COMPLETE - Enhanced Feature Engineering ({train.shape[1]} features)")

