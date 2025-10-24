"""
MILESTONE 1 - Step 1.3.2: Create Lag Features
==============================================
Task 3: Preprocessing and Feature Engineering

Create lag features for time series forecasting:
- Sales from previous weeks (lag 1, 2, 4)
- Rolling statistics (4-week, 8-week moving averages)
- Rolling standard deviation

"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.3.2: CREATE LAG FEATURES")
print("="*80)

print("\n[1] Loading data with time features...")
train = pd.read_csv('processed_data/Stage1.3.1/train_time_features.csv')
test = pd.read_csv('processed_data/Stage1.3.1/test_time_features.csv')
train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])
train = train.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)
test = test.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)
print(f"✓ Loaded: train {train.shape}, test {test.shape}")

print("\n[2] Creating lag features for training data...")
train['Sales_Lag1'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(1)
train['Sales_Lag2'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(2)
train['Sales_Lag4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(4)
train['Sales_Rolling_Mean_4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).mean()
)
train['Sales_Rolling_Mean_8'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=8, min_periods=1).mean()
)
train['Sales_Rolling_Std_4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).std()
)
train['Sales_Momentum'] = train['Weekly_Sales'] - train['Sales_Lag1']
print("✓ Created 7 lag features")

print("\n[3] Handling missing values in lag features...")
lag_features = ['Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4', 'Sales_Rolling_Mean_4', 
                'Sales_Rolling_Mean_8', 'Sales_Rolling_Std_4', 'Sales_Momentum']
for feature in lag_features:
    train[feature] = train[feature].fillna(0)
print("✓ Filled null values with 0")

print("\n[4] Creating lag features for test data...")
combined = pd.concat([train[['Store', 'Dept', 'Date', 'Weekly_Sales']], 
                      test[['Store', 'Dept', 'Date']]], ignore_index=True)
combined = combined.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

combined['Sales_Lag1'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(1)
combined['Sales_Lag2'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(2)
combined['Sales_Lag4'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(4)
combined['Sales_Rolling_Mean_4'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).mean()
)
combined['Sales_Rolling_Mean_8'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=8, min_periods=1).mean()
)
combined['Sales_Rolling_Std_4'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).std()
)
combined['Sales_Momentum'] = combined['Weekly_Sales'] - combined['Sales_Lag1']

test_with_lags = combined[combined['Weekly_Sales'].isna()].copy()
for feature in lag_features:
    test[feature] = test_with_lags[feature].values
    test[feature] = test[feature].fillna(0)
print("✓ Created lag features for test using train history")

print("\n[5] Saving data with lag features...")
output_dir = 'processed_data/Stage1.3.2'
os.makedirs(output_dir, exist_ok=True)
train_output = os.path.join(output_dir, 'train_lag_features.csv')
test_output = os.path.join(output_dir, 'test_lag_features.csv')
train.to_csv(train_output, index=False)
test.to_csv(test_output, index=False)
print(f"✓ Saved: {train_output}, {test_output}")

print("\n" + "="*80)
print("✅ STEP 1.3.2 COMPLETED!")
print("="*80)

