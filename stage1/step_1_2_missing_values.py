"""
MILESTONE 1 - Step 1.2: Handling Missing Values (TRAIN & TEST)
===============================================================
This script handles missing values in both training and test datasets
using identical preprocessing logic for consistency.

Missing Value Strategy:
- MarkDown columns (64-74% missing): Fill with 0 + create binary indicators
- Other columns: Forward/backward fill if needed

"""

import pandas as pd
import numpy as np
import os

def analyze_missing_values(df, dataset_name):
    """Analyze and display missing value statistics"""
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum(),
        'Missing_Percentage': (df.isnull().sum() / len(df) * 100).round(2),
        'Data_Type': df.dtypes
    })
    missing_summary = missing_summary[missing_summary['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    return missing_summary


def handle_missing_values(df, dataset_name):
    """Apply missing value handling strategy to dataset"""
    df_clean = df.copy()
    markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    
    # Create binary indicators
    new_cols = []
    for col in markdown_cols:
        indicator_col = f'Has_{col}'
        df_clean[indicator_col] = df_clean[col].notna().astype(int)
        new_cols.append(indicator_col)
    
    # Fill MarkDown missing values with 0
    for col in markdown_cols:
        df_clean[col] = df_clean[col].fillna(0)
    
    # Handle any other missing values
    remaining_missing = df_clean.isnull().sum().sum()
    if remaining_missing > 0:
        if 'CPI' in df_clean.columns and 'Unemployment' in df_clean.columns:
            if df_clean[['CPI', 'Unemployment']].isnull().sum().sum() > 0:
                df_clean = df_clean.sort_values(['Store', 'Date'])
                df_clean[['CPI', 'Unemployment']] = df_clean.groupby('Store')[['CPI', 'Unemployment']].fillna(method='ffill')
                df_clean[['CPI', 'Unemployment']] = df_clean.groupby('Store')[['CPI', 'Unemployment']].fillna(method='bfill')
    
    return df_clean, new_cols


def display_statistics(df, dataset_name):
    """Display MarkDown statistics after cleaning"""
    markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    for col in markdown_cols:
        non_zero_count = (df[col] > 0).sum()
        non_zero_pct = (non_zero_count / len(df)) * 100


print("STEP 1.2: HANDLING MISSING VALUES")

print("\n[1] Loading datasets...")
train = pd.read_csv('stage1/processed_data/Stage1.1/train_merged.csv')
test = pd.read_csv('stage1/processed_data/Stage1.1/test_merged.csv')
print(f"Loaded: train {train.shape}, test {test.shape}")

print("\n[2] Analyzing missing values...")
train_missing = analyze_missing_values(train, "Training Data")
test_missing = analyze_missing_values(test, "Test Data")

print("\n[3] Processing datasets...")
train_clean, train_new_cols = handle_missing_values(train, "Training Data")
test_clean, test_new_cols = handle_missing_values(test, "Test Data")
print(f"Processed: Added {len(train_new_cols)} indicator columns")

print("\n[4] Saving cleaned datasets...")
output_dir = 'stage1/processed_data/Stage1.2'
os.makedirs(output_dir, exist_ok=True)
train_output = os.path.join(output_dir, 'train_cleaned_step2.csv')
test_output = os.path.join(output_dir, 'test_cleaned_step2.csv')
train_clean.to_csv(train_output, index=False)
test_clean.to_csv(test_output, index=False)
print(f"Saved: {train_output}, {test_output}")

print("\nSTEP 1.2 COMPLETED!")

