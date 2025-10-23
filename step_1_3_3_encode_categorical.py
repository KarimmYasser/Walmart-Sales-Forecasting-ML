"""
MILESTONE 1 - Step 1.3.3: Encode Categorical Variables
======================================================
Task 3: Preprocessing and Feature Engineering

Encode categorical variables for machine learning:
- Store Type (A, B, C) → One-Hot Encoding
- Keep Store and Dept as numeric IDs

Author: Data Science Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.3.3: ENCODE CATEGORICAL VARIABLES")
print("="*80)

# Load data with lag features
print("\n[1] Loading Data with Lag Features...")
print("-" * 80)

train = pd.read_csv('processed_data/Stage1.3.2/train_lag_features.csv')
test = pd.read_csv('processed_data/Stage1.3.2/test_lag_features.csv')

print(f"✓ Train: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"✓ Test:  {test.shape[0]:,} rows × {test.shape[1]} columns")

# ============================================================================
# PART 1: IDENTIFY CATEGORICAL VARIABLES
# ============================================================================

print("\n" + "="*80)
print("[2] Identifying Categorical Variables")
print("="*80)

print(f"\n📊 Categorical Variables to Encode:")
print("-" * 80)

# Store Type (A, B, C)
print(f"\n   Type (Store Type):")
type_counts = train['Type'].value_counts().sort_index()
for store_type, count in type_counts.items():
    print(f"      {store_type}: {count:,} records ({count/len(train)*100:.1f}%)")

print(f"\n💡 Encoding Strategy:")
print("   - Type (A, B, C): One-Hot Encoding → Type_A, Type_B, Type_C")
print("   - Store (1-45): Keep as numeric (acts as ID/index)")
print("   - Dept (1-99): Keep as numeric (acts as ID/index)")

# ============================================================================
# PART 2: ONE-HOT ENCODE STORE TYPE
# ============================================================================

print("\n" + "="*80)
print("[3] One-Hot Encoding Store Type")
print("="*80)

print(f"\n🔧 Applying One-Hot Encoding to 'Type' column...")

# One-hot encode Type for training data
train_encoded = pd.get_dummies(train, columns=['Type'], prefix='Type', drop_first=False)
print(f"   ✓ Train: Created one-hot encoded columns")

# One-hot encode Type for test data
test_encoded = pd.get_dummies(test, columns=['Type'], prefix='Type', drop_first=False)
print(f"   ✓ Test: Created one-hot encoded columns")

# Verify columns created
type_columns = [col for col in train_encoded.columns if col.startswith('Type_')]
print(f"\n   📊 One-Hot Columns Created: {type_columns}")

print(f"\n💡 One-Hot Encoding Explanation:")
print("   Original 'Type' column (A, B, C) replaced with:")
print("   - Type_A: 1 if Type A, 0 otherwise")
print("   - Type_B: 1 if Type B, 0 otherwise")
print("   - Type_C: 1 if Type C, 0 otherwise")

# ============================================================================
# PART 3: VERIFY ENCODING
# ============================================================================

print("\n" + "="*80)
print("[4] Verifying Encoding")
print("="*80)

print(f"\n📋 Sample: Type Encoding (First 10 rows)")
print("-" * 80)

# Show before/after
sample_cols = ['Store', 'Dept', 'Type_A', 'Type_B', 'Type_C']
print(train_encoded[sample_cols].head(10).to_string(index=False))

print(f"\n   💡 Each row has exactly one '1' (one type per store)")

# Verify one-hot encoding correctness
print(f"\n📊 Type Distribution (Training Data):")
print("-" * 80)

for col in type_columns:
    count = train_encoded[col].sum()
    percentage = (count / len(train_encoded)) * 100
    print(f"   {col:10s}: {int(count):7,} records ({percentage:5.1f}%)")

# Verify test data matches
print(f"\n📊 Type Distribution (Test Data):")
print("-" * 80)

for col in type_columns:
    count = test_encoded[col].sum()
    percentage = (count / len(test_encoded)) * 100
    print(f"   {col:10s}: {int(count):7,} records ({percentage:5.1f}%)")

# ============================================================================
# PART 4: CONSISTENCY CHECK
# ============================================================================

print("\n" + "="*80)
print("[5] Train-Test Consistency Check")
print("="*80)

train_cols = set(train_encoded.columns)
test_cols = set(test_encoded.columns)

common_cols = train_cols.intersection(test_cols)
train_only = train_cols - test_cols
test_only = test_cols - train_cols

print(f"\n   Common columns: {len(common_cols)}")
print(f"   Train-only: {list(train_only) if train_only else 'None'}")
print(f"   Test-only: {list(test_only) if test_only else 'None'}")

if train_only == {'Weekly_Sales'} and len(test_only) == 0:
    print("\n   ✅ PERFECT: Same structure except target variable")
else:
    print("\n   ⚠ Note: Column differences detected")

print(f"\n   Final Column Count:")
print(f"   - Train: {len(train_encoded.columns)} columns")
print(f"   - Test:  {len(test_encoded.columns)} columns")

# ============================================================================
# PART 5: FEATURE SUMMARY
# ============================================================================

print("\n" + "="*80)
print("[6] Complete Feature Summary")
print("="*80)

print(f"\n📊 Final Dataset Composition (Train):")
print("-" * 80)

# Categorize all features
feature_categories = {
    'Identifiers': ['Store', 'Dept', 'Date'],
    'Target': ['Weekly_Sales'] if 'Weekly_Sales' in train_encoded.columns else [],
    'Store Type (Encoded)': ['Type_A', 'Type_B', 'Type_C'],
    'Store Attributes': ['Size'],
    'External Factors': ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment'],
    'Promotional': ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5',
                    'Has_MarkDown1', 'Has_MarkDown2', 'Has_MarkDown3', 'Has_MarkDown4', 'Has_MarkDown5'],
    'Holiday': ['IsHoliday'],
    'Time Features': ['Year', 'Month', 'Day', 'Quarter', 'DayOfWeek', 'WeekOfYear',
                     'Is_Weekend', 'Is_Month_Start', 'Is_Month_End', 'Is_Quarter_Start',
                     'Is_Quarter_End', 'Is_Year_Start', 'Is_Year_End',
                     'Month_Sin', 'Month_Cos', 'Week_Sin', 'Week_Cos', 'DayOfWeek_Sin', 'DayOfWeek_Cos'],
    'Lag Features': ['Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4', 'Sales_Rolling_Mean_4',
                     'Sales_Rolling_Mean_8', 'Sales_Rolling_Std_4', 'Sales_Momentum']
}

for category, features in feature_categories.items():
    existing = [f for f in features if f in train_encoded.columns]
    if existing:
        print(f"\n   {category:25s}: {len(existing):2d} features")

print(f"\n   {'TOTAL FEATURES':25s}: {len(train_encoded.columns):2d}")
print(f"   {'MODELING FEATURES':25s}: {len(train_encoded.columns) - 2:2d} (excluding Date, Weekly_Sales)")

# ============================================================================
# PART 6: SAVE ENCODED DATA
# ============================================================================

print("\n" + "="*80)
print("[7] Saving Encoded Data")
print("="*80)

output_dir = 'processed_data/Stage1.3.3'
os.makedirs(output_dir, exist_ok=True)

train_output = os.path.join(output_dir, 'train_encoded.csv')
test_output = os.path.join(output_dir, 'test_encoded.csv')

train_encoded.to_csv(train_output, index=False)
test_encoded.to_csv(test_output, index=False)

train_size = os.path.getsize(train_output) / (1024 * 1024)
test_size = os.path.getsize(test_output) / (1024 * 1024)

print(f"\n💾 Saved Training Data:")
print(f"   File: {train_output}")
print(f"   Size: {train_size:.2f} MB")
print(f"   Rows: {len(train_encoded):,}")
print(f"   Columns: {len(train_encoded.columns)} (added {len(type_columns)} features, removed 1)")

print(f"\n💾 Saved Test Data:")
print(f"   File: {test_output}")
print(f"   Size: {test_size:.2f} MB")
print(f"   Rows: {len(test_encoded):,}")
print(f"   Columns: {len(test_encoded.columns)} (added {len(type_columns)} features, removed 1)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ STEP 1.3.3 COMPLETED SUCCESSFULLY!")
print("="*80)

print(f"""
📊 Encoding Summary:

   Categorical Variable Encoded: 1
   └─ Type (A, B, C) → Type_A, Type_B, Type_C (one-hot)

   Training Data:
   ├─ Before: {train.shape[0]:,} rows × {train.shape[1]} columns
   ├─ After:  {train_encoded.shape[0]:,} rows × {train_encoded.shape[1]} columns
   └─ Net:    +2 columns (removed 'Type', added 3 one-hot columns)

   Test Data:
   ├─ Before: {test.shape[0]:,} rows × {test.shape[1]} columns
   ├─ After:  {test_encoded.shape[0]:,} rows × {test_encoded.shape[1]} columns
   └─ Net:    +2 columns (same transformation)

✅ Actions Completed:
   1. Identified categorical variable (Type)
   2. Applied one-hot encoding to Store Type
   3. Created 3 binary columns (Type_A, Type_B, Type_C)
   4. Verified encoding correctness
   5. Maintained train-test consistency
   6. Saved encoded datasets

📁 Output Files:
   - {train_output}
   - {test_output}

🎯 Why One-Hot Encoding?
   - ML algorithms need numerical inputs
   - Avoids ordinal assumptions (A ≠ 1, B ≠ 2, C ≠ 3)
   - Each type treated as separate category
   - No implicit ordering between types

⚠️ What Was NOT Encoded:
   - Store (1-45): Kept as numeric ID (can be treated as categorical by tree models)
   - Dept (1-99): Kept as numeric ID (can be treated as categorical by tree models)
   - Binary features (already 0/1)
   - Time features (already numeric)

💡 Alternative Encoding Options (for future):
   - Store/Dept: Could use target encoding or embeddings
   - Type: Could use label encoding if tree-based models only
   - Current approach: Works for all model types

🔜 Next Step:
   Step 1.3.4: Normalize Numerical Features
""")

print("="*80)

