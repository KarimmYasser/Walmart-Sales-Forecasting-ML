"""
MILESTONE 1 - Step 1.2: Handling Missing Values
================================================
This script handles missing values in the merged Walmart dataset.

Missing Value Strategy:
- MarkDown columns (64-74% missing): Fill with 0 + create binary indicators
- Other columns: Already complete

Author: Data Science Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.2: HANDLING MISSING VALUES")
print("="*80)

# Load the merged training data
print("\n[1] Loading Merged Training Data...")
print("-" * 80)

train = pd.read_csv('processed_data/train_merged.csv')
print(f"✓ Loaded: {train.shape[0]:,} rows × {train.shape[1]} columns")

# Analyze missing values
print("\n[2] Missing Values Analysis")
print("="*80)

print("\n📊 Current Missing Value Status:")
missing_summary = pd.DataFrame({
    'Column': train.columns,
    'Missing_Count': train.isnull().sum(),
    'Missing_Percentage': (train.isnull().sum() / len(train) * 100).round(2),
    'Data_Type': train.dtypes
})
missing_summary = missing_summary[missing_summary['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)

if len(missing_summary) > 0:
    print("\nColumns with Missing Values:")
    print("-" * 80)
    for idx, row in missing_summary.iterrows():
        print(f"   {row['Column']:20s} | Missing: {row['Missing_Count']:7,} ({row['Missing_Percentage']:5.1f}%) | Type: {row['Data_Type']}")
else:
    print("   ✓ No missing values found!")

# Detailed analysis of MarkDown columns
print("\n" + "="*80)
print("[3] MarkDown Columns Analysis")
print("="*80)

markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']

print("\n📈 MarkDown Statistics (Non-Null Values Only):")
print("-" * 80)
for col in markdown_cols:
    non_null = train[col].dropna()
    if len(non_null) > 0:
        print(f"\n{col}:")
        print(f"   Non-null count: {len(non_null):,} ({(len(non_null)/len(train)*100):.1f}%)")
        print(f"   Mean: ${non_null.mean():,.2f}")
        print(f"   Median: ${non_null.median():,.2f}")
        print(f"   Min: ${non_null.min():,.2f}")
        print(f"   Max: ${non_null.max():,.2f}")
        print(f"   Std Dev: ${non_null.std():,.2f}")

print("\n" + "-" * 80)
print("💡 Interpretation:")
print("   - MarkDown columns have 64-74% missing values")
print("   - Missing values indicate NO promotional markdown that week")
print("   - This is expected business behavior (not all weeks have promotions)")
print("   - Strategy: Fill with 0 AND create binary indicators")

# Strategy Selection
print("\n" + "="*80)
print("[4] Missing Value Handling Strategy")
print("="*80)

print("\n📋 Strategy for MarkDown Columns:")
print("   1. Fill missing values with 0 (no promotion)")
print("   2. Create binary indicator columns (Has_MarkDownX)")
print("   3. Keep both original and indicator columns for model flexibility")

print("\n📋 Strategy for Other Columns:")
other_missing = missing_summary[~missing_summary['Column'].isin(markdown_cols)]
if len(other_missing) > 0:
    print("   ⚠ Found missing values in non-MarkDown columns:")
    for idx, row in other_missing.iterrows():
        print(f"   - {row['Column']}: {row['Missing_Count']:,} missing")
    print("   Action: Will apply forward fill by Store")
else:
    print("   ✓ No missing values in other columns - all clean!")

# Implement the strategy
print("\n" + "="*80)
print("[5] Implementing Missing Value Handling")
print("="*80)

# Create a copy for processing
train_clean = train.copy()

# Step 1: Create binary indicators for MarkDown columns
print("\n🔧 Step 5.1: Creating Binary Indicators...")
for col in markdown_cols:
    indicator_col = f'Has_{col}'
    train_clean[indicator_col] = train_clean[col].notna().astype(int)
    has_count = train_clean[indicator_col].sum()
    print(f"   ✓ Created {indicator_col:20s} | Weeks with promotion: {has_count:,} ({has_count/len(train_clean)*100:.1f}%)")

# Step 2: Fill MarkDown missing values with 0
print("\n🔧 Step 5.2: Filling MarkDown Missing Values with 0...")
for col in markdown_cols:
    before_null = train_clean[col].isnull().sum()
    train_clean[col].fillna(0, inplace=True)
    after_null = train_clean[col].isnull().sum()
    print(f"   ✓ {col:15s} | Before: {before_null:7,} nulls → After: {after_null:7,} nulls | Filled: {before_null - after_null:7,}")

# Step 3: Handle any other missing values (if they exist)
print("\n🔧 Step 5.3: Checking for Remaining Missing Values...")
remaining_missing = train_clean.isnull().sum().sum()
if remaining_missing > 0:
    print(f"   ⚠ Found {remaining_missing:,} remaining missing values")
    
    # Forward fill by Store for CPI and Unemployment if needed
    if train_clean[['CPI', 'Unemployment']].isnull().sum().sum() > 0:
        print("   Applying forward fill by Store for CPI and Unemployment...")
        train_clean = train_clean.sort_values(['Store', 'Date'])
        train_clean[['CPI', 'Unemployment']] = train_clean.groupby('Store')[['CPI', 'Unemployment']].fillna(method='ffill')
        train_clean[['CPI', 'Unemployment']] = train_clean.groupby('Store')[['CPI', 'Unemployment']].fillna(method='bfill')
        print(f"   ✓ After forward/backward fill: {train_clean[['CPI', 'Unemployment']].isnull().sum().sum()} nulls remaining")
else:
    print("   ✓ No remaining missing values - dataset is complete!")

# Verification
print("\n" + "="*80)
print("[6] Verification & Quality Check")
print("="*80)

print("\n📊 Final Missing Value Check:")
final_missing = train_clean.isnull().sum()
if final_missing.sum() == 0:
    print("   ✅ SUCCESS: No missing values remaining in dataset!")
else:
    print("   ⚠ WARNING: Still have missing values:")
    for col in final_missing[final_missing > 0].index:
        print(f"      - {col}: {final_missing[col]:,} missing ({final_missing[col]/len(train_clean)*100:.2f}%)")

print("\n📊 Dataset Shape:")
print(f"   Before: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"   After:  {train_clean.shape[0]:,} rows × {train_clean.shape[1]} columns")
print(f"   Added:  {train_clean.shape[1] - train.shape[1]} new columns (binary indicators)")

print("\n📊 New Columns Added:")
new_cols = [col for col in train_clean.columns if col not in train.columns]
for i, col in enumerate(new_cols, 1):
    print(f"   {i}. {col}")

# Sample data check
print("\n" + "="*80)
print("[7] Sample Data Verification")
print("="*80)

print("\n📋 Sample: Store 1, Dept 1 (First 10 weeks)")
sample_cols = ['Store', 'Dept', 'Date', 'MarkDown1', 'Has_MarkDown1', 'MarkDown2', 'Has_MarkDown2', 'Weekly_Sales']
sample = train_clean[(train_clean['Store'] == 1) & (train_clean['Dept'] == 1)][sample_cols].head(10)
print(sample.to_string(index=False))

print("\n💡 Interpretation:")
print("   - MarkDown values are now 0 when there's no promotion")
print("   - Has_MarkDown indicators show 1 when promotion exists, 0 otherwise")
print("   - Models can use both: actual markdown amount AND promotion presence")

# Statistics after cleaning
print("\n" + "="*80)
print("[8] Post-Cleaning Statistics")
print("="*80)

print("\n📊 MarkDown Statistics (After Filling):")
print("-" * 80)
for col in markdown_cols:
    print(f"\n{col}:")
    print(f"   Mean: ${train_clean[col].mean():,.2f}")
    print(f"   Median: ${train_clean[col].median():,.2f}")
    print(f"   Non-zero count: {(train_clean[col] > 0).sum():,} ({(train_clean[col] > 0).sum()/len(train_clean)*100:.1f}%)")
    print(f"   Zero count: {(train_clean[col] == 0).sum():,} ({(train_clean[col] == 0).sum()/len(train_clean)*100:.1f}%)")

# Save cleaned data
print("\n" + "="*80)
print("[9] Saving Cleaned Dataset")
print("="*80)

output_file = 'processed_data/train_cleaned_step2.csv'
train_clean.to_csv(output_file, index=False)
file_size = os.path.getsize(output_file) / (1024 * 1024)

print(f"\n💾 Saved cleaned dataset:")
print(f"   File: {output_file}")
print(f"   Size: {file_size:.2f} MB")
print(f"   Rows: {len(train_clean):,}")
print(f"   Columns: {len(train_clean.columns)}")

# Summary
print("\n" + "="*80)
print("✅ STEP 1.2 COMPLETED SUCCESSFULLY!")
print("="*80)

print(f"""
📊 Summary:
   - Loaded data: {train.shape[0]:,} rows × {train.shape[1]} columns
   - Handled {len(markdown_cols)} MarkDown columns with {(train[markdown_cols].isnull().sum().sum() / (len(train) * len(markdown_cols)) * 100):.1f}% missing values
   - Created {len(new_cols)} binary indicator columns
   - Final dataset: {train_clean.shape[0]:,} rows × {train_clean.shape[1]} columns
   - Missing values: {train_clean.isnull().sum().sum()} (0%)
   
✅ Actions Completed:
   1. Analyzed missing value patterns
   2. Filled MarkDown columns with 0
   3. Created Has_MarkDown binary indicators
   4. Verified data quality
   5. Saved cleaned dataset

📁 Output:
   - {output_file}
   
🔜 Next Step:
   - Step 1.3: Outlier Detection & Handling
""")

print("="*80)

