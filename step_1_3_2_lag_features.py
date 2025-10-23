"""
MILESTONE 1 - Step 1.3.2: Create Lag Features
==============================================
Task 3: Preprocessing and Feature Engineering

Create lag features for time series forecasting:
- Sales from previous weeks (lag 1, 2, 4)
- Rolling statistics (4-week, 8-week moving averages)
- Rolling standard deviation

Author: Data Science Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.3.2: CREATE LAG FEATURES")
print("="*80)

# Load data with time features
print("\n[1] Loading Data with Time Features...")
print("-" * 80)

train = pd.read_csv('processed_data/Stage1.3.1/train_time_features.csv')
test = pd.read_csv('processed_data/Stage1.3.1/test_time_features.csv')

print(f"✓ Train: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"✓ Test:  {test.shape[0]:,} rows × {test.shape[1]} columns")

# Convert Date to datetime and sort
train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])

train = train.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)
test = test.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

print(f"\n   ✓ Data sorted by Store, Dept, Date")

# ============================================================================
# PART 1: CREATE LAG FEATURES (TRAINING DATA ONLY)
# ============================================================================

print("\n" + "="*80)
print("[2] Creating Lag Features for Training Data")
print("="*80)

print("\n🔧 Creating lag features by Store-Department combination...")
print("   (Each store-dept has its own sales history)")

# Lag features (previous weeks' sales)
train['Sales_Lag1'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(1)
train['Sales_Lag2'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(2)
train['Sales_Lag4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(4)

print(f"   ✓ Created Sales_Lag1 (1 week ago)")
print(f"   ✓ Created Sales_Lag2 (2 weeks ago)")
print(f"   ✓ Created Sales_Lag4 (4 weeks ago)")

# Rolling statistics
train['Sales_Rolling_Mean_4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).mean()
)
train['Sales_Rolling_Mean_8'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=8, min_periods=1).mean()
)
train['Sales_Rolling_Std_4'] = train.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).std()
)

print(f"   ✓ Created Sales_Rolling_Mean_4 (4-week moving average)")
print(f"   ✓ Created Sales_Rolling_Mean_8 (8-week moving average)")
print(f"   ✓ Created Sales_Rolling_Std_4 (4-week rolling std dev)")

# Sales momentum (difference from previous week)
train['Sales_Momentum'] = train['Weekly_Sales'] - train['Sales_Lag1']

print(f"   ✓ Created Sales_Momentum (change from last week)")

print(f"\n   📊 Total lag features created: 7")

# ============================================================================
# PART 2: CHECK FOR NULL VALUES
# ============================================================================

print("\n" + "="*80)
print("[3] Handling Missing Values in Lag Features")
print("="*80)

lag_features = ['Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4', 'Sales_Rolling_Mean_4', 
                'Sales_Rolling_Mean_8', 'Sales_Rolling_Std_4', 'Sales_Momentum']

print(f"\n📊 Missing Values in Lag Features:")
print("-" * 80)

for feature in lag_features:
    null_count = train[feature].isnull().sum()
    null_pct = (null_count / len(train)) * 100
    print(f"   {feature:25s}: {null_count:7,} ({null_pct:5.2f}%)")

print(f"\n💡 Why are there nulls?")
print("   - Lag1: First week for each Store-Dept has no previous week")
print("   - Lag2: First 2 weeks have no 2-week history")
print("   - Lag4: First 4 weeks have no 4-week history")
print("   - Rolling stats: Early weeks have limited history")

print(f"\n🔧 Strategy: Fill nulls with 0 (indicates start of time series)")
for feature in lag_features:
    train[feature] = train[feature].fillna(0)

print(f"   ✓ All lag feature nulls filled with 0")

# ============================================================================
# PART 3: TEST DATA LAG FEATURES
# ============================================================================

print("\n" + "="*80)
print("[4] Creating Lag Features for Test Data")
print("="*80)

print("\n⚠️  IMPORTANT: Test data needs historical sales from training data!")
print("   Test period: Nov 2012 - Jul 2013")
print("   Need: Oct 2012 sales for Lag1, Sep-Oct for Lag2, etc.")

# Combine train and test temporarily to create proper lags
print(f"\n🔧 Strategy: Use last weeks of training data for test lags...")

# Get the last few weeks from training for each Store-Dept
train_tail = train.groupby(['Store', 'Dept']).tail(8)[['Store', 'Dept', 'Date', 'Weekly_Sales']]

# Combine for lag calculation
combined = pd.concat([train[['Store', 'Dept', 'Date', 'Weekly_Sales']], 
                      test[['Store', 'Dept', 'Date']]], ignore_index=True)
combined = combined.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

print(f"   ✓ Combined train + test: {len(combined):,} rows")

# Create lag features on combined data
combined['Sales_Lag1'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(1)
combined['Sales_Lag2'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(2)
combined['Sales_Lag4'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].shift(4)

# Rolling statistics on combined data
combined['Sales_Rolling_Mean_4'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).mean()
)
combined['Sales_Rolling_Mean_8'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=8, min_periods=1).mean()
)
combined['Sales_Rolling_Std_4'] = combined.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
    lambda x: x.rolling(window=4, min_periods=1).std()
)

# Sales momentum
combined['Sales_Momentum'] = combined['Weekly_Sales'] - combined['Sales_Lag1']

# Extract test portion with lag features
test_with_lags = combined[combined['Weekly_Sales'].isna()].copy()

# Add lag features to test data
for feature in lag_features:
    test[feature] = test_with_lags[feature].values

print(f"   ✓ Created lag features for test data using train history")

# Fill any remaining nulls in test
for feature in lag_features:
    null_count_before = test[feature].isnull().sum()
    test[feature] = test[feature].fillna(0)
    if null_count_before > 0:
        print(f"   ✓ Filled {null_count_before:,} nulls in {feature}")

# ============================================================================
# PART 4: VERIFY LAG FEATURES
# ============================================================================

print("\n" + "="*80)
print("[5] Verifying Lag Features")
print("="*80)

print(f"\n📋 Sample: Store 1, Dept 1 (First 10 weeks)")
print("-" * 80)

sample_cols = ['Date', 'Weekly_Sales', 'Sales_Lag1', 'Sales_Lag2', 'Sales_Rolling_Mean_4']
sample = train[(train['Store'] == 1) & (train['Dept'] == 1)][sample_cols].head(10)
print(sample.to_string(index=False))

print(f"\n💡 Observations:")
print("   - Week 1: Lag1=0 (no previous week)")
print("   - Week 2: Lag1 = Week 1 sales")
print("   - Week 3: Lag1 = Week 2 sales, Lag2 = Week 1 sales")
print("   - Rolling mean gradually incorporates more history")

print(f"\n📊 Lag Feature Statistics (Training Data):")
print("-" * 80)

for feature in lag_features:
    mean_val = train[feature].mean()
    std_val = train[feature].std()
    min_val = train[feature].min()
    max_val = train[feature].max()
    print(f"   {feature:25s} | Mean: ${mean_val:>10,.2f} | Std: ${std_val:>10,.2f} | Range: [${min_val:>10,.2f}, ${max_val:>12,.2f}]")

# ============================================================================
# PART 5: SAVE DATA WITH LAG FEATURES
# ============================================================================

print("\n" + "="*80)
print("[6] Saving Data with Lag Features")
print("="*80)

output_dir = 'processed_data/Stage1.3.2'
os.makedirs(output_dir, exist_ok=True)

train_output = os.path.join(output_dir, 'train_lag_features.csv')
test_output = os.path.join(output_dir, 'test_lag_features.csv')

train.to_csv(train_output, index=False)
test.to_csv(test_output, index=False)

train_size = os.path.getsize(train_output) / (1024 * 1024)
test_size = os.path.getsize(test_output) / (1024 * 1024)

print(f"\n💾 Saved Training Data:")
print(f"   File: {train_output}")
print(f"   Size: {train_size:.2f} MB")
print(f"   Rows: {len(train):,}")
print(f"   Columns: {len(train.columns)} (added 7 lag features)")

print(f"\n💾 Saved Test Data:")
print(f"   File: {test_output}")
print(f"   Size: {test_size:.2f} MB")
print(f"   Rows: {len(test):,}")
print(f"   Columns: {len(test.columns)} (added 7 lag features)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ STEP 1.3.2 COMPLETED SUCCESSFULLY!")
print("="*80)

print(f"""
📊 Lag Features Summary:

   Features Created: 7
   ├─ Lag Features:    3 (Sales_Lag1, Sales_Lag2, Sales_Lag4)
   ├─ Rolling Means:   2 (4-week MA, 8-week MA)
   ├─ Rolling Std:     1 (4-week std dev)
   └─ Momentum:        1 (change from last week)

   Training Data:
   ├─ Before: {train.shape[0]:,} rows × {train.shape[1] - 7} columns
   ├─ After:  {train.shape[0]:,} rows × {train.shape[1]} columns
   └─ Added:  7 lag features

   Test Data:
   ├─ Before: {test.shape[0]:,} rows × {test.shape[1] - 7} columns
   ├─ After:  {test.shape[0]:,} rows × {test.shape[1]} columns
   └─ Added:  7 lag features (using train history)

✅ Actions Completed:
   1. Created 3 lag features (1, 2, 4 weeks back)
   2. Created 2 rolling averages (4-week, 8-week)
   3. Created rolling standard deviation (4-week)
   4. Created sales momentum feature
   5. Handled nulls (filled with 0)
   6. Applied to both train and test datasets
   7. Used train history for test lag features

📁 Output Files:
   - {train_output}
   - {test_output}

🎯 Why Lag Features Matter:
   - Capture temporal dependencies (sales patterns over time)
   - Yesterday's sales predict today's sales
   - Rolling averages smooth out noise
   - Momentum captures trends (increasing/decreasing)
   - Critical for time series forecasting

⚠️ Important Notes:
   - Lag features grouped by Store-Dept (each has own history)
   - Test data uses training data for lag calculation
   - First few weeks have nulls (filled with 0)
   - Features capture recent history (1-8 weeks)

🔜 Next Step:
   Step 1.3.3: Encode Categorical Variables (Type: A/B/C)
""")

print("="*80)

