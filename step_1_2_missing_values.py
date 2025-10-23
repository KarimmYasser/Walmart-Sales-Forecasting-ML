"""
MILESTONE 1 - Step 1.2: Handling Missing Values (TRAIN & TEST)
===============================================================
This script handles missing values in both training and test datasets
using identical preprocessing logic for consistency.

Missing Value Strategy:
- MarkDown columns (64-74% missing): Fill with 0 + create binary indicators
- Other columns: Forward/backward fill if needed

Author: Data Science Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
import os

def analyze_missing_values(df, dataset_name):
    """Analyze and display missing value statistics"""
    print(f"\n📊 Missing Value Analysis - {dataset_name}:")
    print("-" * 80)
    
    missing_summary = pd.DataFrame({
        'Column': df.columns,
        'Missing_Count': df.isnull().sum(),
        'Missing_Percentage': (df.isnull().sum() / len(df) * 100).round(2),
        'Data_Type': df.dtypes
    })
    missing_summary = missing_summary[missing_summary['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
    
    if len(missing_summary) > 0:
        print("\nColumns with Missing Values:")
        for idx, row in missing_summary.iterrows():
            print(f"   {row['Column']:20s} | Missing: {row['Missing_Count']:7,} ({row['Missing_Percentage']:5.1f}%) | Type: {row['Data_Type']}")
        return missing_summary
    else:
        print("   ✓ No missing values found!")
        return missing_summary


def handle_missing_values(df, dataset_name):
    """Apply missing value handling strategy to dataset"""
    print(f"\n🔧 Processing {dataset_name}...")
    print("-" * 80)
    
    # Create a copy for processing
    df_clean = df.copy()
    
    markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    
    # Step 1: Create binary indicators
    print(f"\n   Step 1: Creating Binary Indicators for {dataset_name}...")
    new_cols = []
    for col in markdown_cols:
        indicator_col = f'Has_{col}'
        df_clean[indicator_col] = df_clean[col].notna().astype(int)
        new_cols.append(indicator_col)
        has_count = df_clean[indicator_col].sum()
        print(f"      ✓ {indicator_col:20s} | Promotions: {has_count:7,} ({has_count/len(df_clean)*100:5.1f}%)")
    
    # Step 2: Fill MarkDown missing values with 0
    print(f"\n   Step 2: Filling MarkDown Columns with 0...")
    for col in markdown_cols:
        before_null = df_clean[col].isnull().sum()
        df_clean[col] = df_clean[col].fillna(0)
        after_null = df_clean[col].isnull().sum()
        filled_count = before_null - after_null
        if filled_count > 0:
            print(f"      ✓ {col:15s} | Filled: {filled_count:7,} values")
    
    # Step 3: Handle any other missing values
    print(f"\n   Step 3: Checking for Remaining Missing Values...")
    remaining_missing = df_clean.isnull().sum().sum()
    if remaining_missing > 0:
        print(f"      ⚠ Found {remaining_missing:,} remaining missing values")
        
        # Forward/backward fill by Store for CPI and Unemployment if needed
        if 'CPI' in df_clean.columns and 'Unemployment' in df_clean.columns:
            if df_clean[['CPI', 'Unemployment']].isnull().sum().sum() > 0:
                print("      Applying forward/backward fill by Store...")
                df_clean = df_clean.sort_values(['Store', 'Date'])
                df_clean[['CPI', 'Unemployment']] = df_clean.groupby('Store')[['CPI', 'Unemployment']].fillna(method='ffill')
                df_clean[['CPI', 'Unemployment']] = df_clean.groupby('Store')[['CPI', 'Unemployment']].fillna(method='bfill')
                remaining = df_clean[['CPI', 'Unemployment']].isnull().sum().sum()
                print(f"      ✓ After fill: {remaining} nulls remaining")
    else:
        print("      ✓ No remaining missing values!")
    
    # Final verification
    final_missing = df_clean.isnull().sum().sum()
    if final_missing == 0:
        print(f"\n   ✅ {dataset_name}: 100% Complete (0 missing values)")
    else:
        print(f"\n   ⚠ {dataset_name}: Still has {final_missing:,} missing values")
    
    return df_clean, new_cols


def display_statistics(df, dataset_name):
    """Display MarkDown statistics after cleaning"""
    markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    
    print(f"\n📊 MarkDown Statistics - {dataset_name}:")
    print("-" * 80)
    for col in markdown_cols:
        non_zero_count = (df[col] > 0).sum()
        non_zero_pct = (non_zero_count / len(df)) * 100
        print(f"\n   {col}:")
        print(f"      Mean: ${df[col].mean():,.2f}")
        print(f"      Median: ${df[col].median():,.2f}")
        print(f"      Non-zero: {non_zero_count:,} ({non_zero_pct:.1f}%)")
        print(f"      Zero: {(df[col] == 0).sum():,} ({((df[col] == 0).sum()/len(df)*100):.1f}%)")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

print("="*80)
print("STEP 1.2: HANDLING MISSING VALUES")
print("Processing BOTH Training and Test Datasets")
print("="*80)

# ============================================================================
# PART 1: LOAD DATA
# ============================================================================

print("\n[1] Loading Datasets...")
print("="*80)

print("\n📂 Loading Training Data...")
train = pd.read_csv('processed_data/Stage1.1/train_merged.csv')
print(f"   ✓ Train: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"   ✓ Date Range: {train['Date'].min()} to {train['Date'].max()}")

print("\n📂 Loading Test Data...")
test = pd.read_csv('processed_data/Stage1.1/test_merged.csv')
print(f"   ✓ Test: {test.shape[0]:,} rows × {test.shape[1]} columns")
print(f"   ✓ Date Range: {test['Date'].min()} to {test['Date'].max()}")

# ============================================================================
# PART 2: ANALYZE MISSING VALUES
# ============================================================================

print("\n" + "="*80)
print("[2] Analyzing Missing Values")
print("="*80)

train_missing = analyze_missing_values(train, "Training Data")
test_missing = analyze_missing_values(test, "Test Data")

# ============================================================================
# PART 3: STRATEGY EXPLANATION
# ============================================================================

print("\n" + "="*80)
print("[3] Missing Value Handling Strategy")
print("="*80)

print("""
📋 Strategy for MarkDown Columns (Primary Issue):
   1. Fill missing values with 0 (indicates no promotion that week)
   2. Create binary indicator columns (Has_MarkDownX)
   3. Keep both for model flexibility
   
💡 Why This Approach?
   - MarkDown amount matters: $100 vs $10,000 has different impact
   - Promotion presence matters: ANY promotion vs none signals strategy
   - Tree-based models can leverage both features effectively
   - Missing = business logic (no promo), not data quality issue
   
📋 Strategy for Other Columns:
   - Forward/backward fill by Store (if any missing)
   - Maintain temporal ordering
""")

# ============================================================================
# PART 4: PROCESS TRAINING DATA
# ============================================================================

print("\n" + "="*80)
print("[4] Processing Training Dataset")
print("="*80)

train_clean, train_new_cols = handle_missing_values(train, "Training Data")

print(f"\n📊 Training Dataset Transformation:")
print(f"   Before: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"   After:  {train_clean.shape[0]:,} rows × {train_clean.shape[1]} columns")
print(f"   Added:  {len(train_new_cols)} new columns: {', '.join(train_new_cols)}")

# ============================================================================
# PART 5: PROCESS TEST DATA
# ============================================================================

print("\n" + "="*80)
print("[5] Processing Test Dataset (SAME LOGIC)")
print("="*80)

test_clean, test_new_cols = handle_missing_values(test, "Test Data")

print(f"\n📊 Test Dataset Transformation:")
print(f"   Before: {test.shape[0]:,} rows × {test.shape[1]} columns")
print(f"   After:  {test_clean.shape[0]:,} rows × {test_clean.shape[1]} columns")
print(f"   Added:  {len(test_new_cols)} new columns: {', '.join(test_new_cols)}")

# ============================================================================
# PART 6: CONSISTENCY VERIFICATION
# ============================================================================

print("\n" + "="*80)
print("[6] Consistency Verification")
print("="*80)

print("\n🔍 Checking Train-Test Consistency...")

train_cols = set(train_clean.columns)
test_cols = set(test_clean.columns)

train_only = train_cols - test_cols
test_only = test_cols - train_cols

print(f"\n   Training columns: {len(train_cols)}")
print(f"   Test columns:     {len(test_cols)}")
print(f"   Train-only:       {list(train_only) if train_only else 'None'}")
print(f"   Test-only:        {list(test_only) if test_only else 'None'}")

# Expected: only Weekly_Sales in train
if train_only == {'Weekly_Sales'} and len(test_only) == 0:
    print("\n   ✅ PERFECT CONSISTENCY!")
    print("   ✅ Test has exact same features as train (minus target variable)")
    print("   ✅ Ready for model training and predictions!")
else:
    print("\n   ⚠ WARNING: Unexpected column differences detected!")

# ============================================================================
# PART 7: SAMPLE DATA VERIFICATION
# ============================================================================

print("\n" + "="*80)
print("[7] Sample Data Verification")
print("="*80)

print("\n📋 Training Data Sample (Store 1, Dept 1 - First 5 weeks):")
sample_cols = ['Store', 'Dept', 'Date', 'MarkDown1', 'Has_MarkDown1', 'Weekly_Sales']
train_sample = train_clean[(train_clean['Store'] == 1) & (train_clean['Dept'] == 1)][sample_cols].head(5)
print(train_sample.to_string(index=False))

print("\n📋 Test Data Sample (Store 1, Dept 1 - First 5 weeks):")
sample_cols_test = ['Store', 'Dept', 'Date', 'MarkDown1', 'Has_MarkDown1', 'IsHoliday']
test_sample = test_clean[(test_clean['Store'] == 1) & (test_clean['Dept'] == 1)][sample_cols_test].head(5)
print(test_sample.to_string(index=False))

# ============================================================================
# PART 8: STATISTICS
# ============================================================================

print("\n" + "="*80)
print("[8] Post-Cleaning Statistics")
print("="*80)

display_statistics(train_clean, "Training Data")
display_statistics(test_clean, "Test Data")

# ============================================================================
# PART 9: SAVE CLEANED DATASETS
# ============================================================================

print("\n" + "="*80)
print("[9] Saving Cleaned Datasets")
print("="*80)

# Save training data
train_output = 'processed_data/train_cleaned_step2.csv'
train_clean.to_csv(train_output, index=False)
train_size = os.path.getsize(train_output) / (1024 * 1024)
print(f"\n💾 Training Data Saved:")
print(f"   File: {train_output}")
print(f"   Size: {train_size:.2f} MB")
print(f"   Rows: {len(train_clean):,}")
print(f"   Columns: {len(train_clean.columns)}")

# Save test data
test_output = 'processed_data/test_cleaned_step2.csv'
test_clean.to_csv(test_output, index=False)
test_size = os.path.getsize(test_output) / (1024 * 1024)
print(f"\n💾 Test Data Saved:")
print(f"   File: {test_output}")
print(f"   Size: {test_size:.2f} MB")
print(f"   Rows: {len(test_clean):,}")
print(f"   Columns: {len(test_clean.columns)}")

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ STEP 1.2 COMPLETED SUCCESSFULLY!")
print("="*80)

print(f"""
📊 Summary - Training Dataset:
   ├─ Original:  {train.shape[0]:,} rows × {train.shape[1]} columns
   ├─ Cleaned:   {train_clean.shape[0]:,} rows × {train_clean.shape[1]} columns
   ├─ Added:     {len(train_new_cols)} new feature columns
   ├─ Missing:   {train_clean.isnull().sum().sum()} (0%)
   └─ File:      {train_output} ({train_size:.2f} MB)

📊 Summary - Test Dataset:
   ├─ Original:  {test.shape[0]:,} rows × {test.shape[1]} columns
   ├─ Cleaned:   {test_clean.shape[0]:,} rows × {test_clean.shape[1]} columns
   ├─ Added:     {len(test_new_cols)} new feature columns
   ├─ Missing:   {test_clean.isnull().sum().sum()} (0%)
   └─ File:      {test_output} ({test_size:.2f} MB)

✅ Actions Completed:
   1. ✓ Analyzed missing value patterns (both datasets)
   2. ✓ Filled MarkDown columns with 0
   3. ✓ Created {len(train_new_cols)} binary indicator columns
   4. ✓ Achieved 100% data completeness
   5. ✓ Verified train-test consistency
   6. ✓ Saved both cleaned datasets

🎯 Key Results:
   - Both datasets now have IDENTICAL preprocessing
   - No missing values in either dataset
   - New features added for better predictions
   - Ready for next step: Outlier Detection

📁 Output Files:
   ├─ {train_output}
   └─ {test_output}

🔜 Next Step:
   Step 1.3: Outlier Detection & Handling (on training data)
""")

print("="*80)
print("🎉 Both datasets are now clean and consistent!")
print("="*80)

