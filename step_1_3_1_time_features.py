"""
MILESTONE 1 - Step 1.3.1: Create Time-Based Features
====================================================
Task 3: Preprocessing and Feature Engineering

Create time-based features from Date column:
- Month, Week, Day, Quarter, DayOfWeek, WeekOfYear
- Is_Weekend, Is_Month_Start, Is_Month_End
- Year (for trend analysis)

Author: Data Science Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
import os

print("="*80)
print("STEP 1.3.1: CREATE TIME-BASED FEATURES")
print("="*80)

# Load cleaned data
print("\n[1] Loading Cleaned Data...")
print("-" * 80)

train = pd.read_csv('processed_data/Stage1.2/train_cleaned_step2.csv')
test = pd.read_csv('processed_data/Stage1.2/test_cleaned_step2.csv')

print(f"✓ Train: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"✓ Test:  {test.shape[0]:,} rows × {test.shape[1]} columns")

# Convert Date to datetime
train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])

print(f"\n   Train Date Range: {train['Date'].min().date()} to {train['Date'].max().date()}")
print(f"   Test Date Range:  {test['Date'].min().date()} to {test['Date'].max().date()}")

# ============================================================================
# PART 1: CREATE TIME-BASED FEATURES (BOTH TRAIN AND TEST)
# ============================================================================

print("\n" + "="*80)
print("[2] Creating Time-Based Features")
print("="*80)

def create_time_features(df, dataset_name):
    """Create time-based features from Date column"""
    print(f"\n🔧 Processing {dataset_name}...")
    
    # Basic time components
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Quarter'] = df['Date'].dt.quarter
    df['DayOfWeek'] = df['Date'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['WeekOfYear'] = df['Date'].dt.isocalendar().week
    
    # Binary indicators
    df['Is_Weekend'] = (df['DayOfWeek'] >= 5).astype(int)  # Saturday=5, Sunday=6
    df['Is_Month_Start'] = df['Date'].dt.is_month_start.astype(int)
    df['Is_Month_End'] = df['Date'].dt.is_month_end.astype(int)
    df['Is_Quarter_Start'] = df['Date'].dt.is_quarter_start.astype(int)
    df['Is_Quarter_End'] = df['Date'].dt.is_quarter_end.astype(int)
    df['Is_Year_Start'] = df['Date'].dt.is_year_start.astype(int)
    df['Is_Year_End'] = df['Date'].dt.is_year_end.astype(int)
    
    # Cyclical features (for capturing seasonality)
    # Month as sine/cosine (to capture cyclical nature)
    df['Month_Sin'] = np.sin(2 * np.pi * df['Month'] / 12)
    df['Month_Cos'] = np.cos(2 * np.pi * df['Month'] / 12)
    
    # Week as sine/cosine
    df['Week_Sin'] = np.sin(2 * np.pi * df['WeekOfYear'] / 52)
    df['Week_Cos'] = np.cos(2 * np.pi * df['WeekOfYear'] / 52)
    
    # Day of week as sine/cosine
    df['DayOfWeek_Sin'] = np.sin(2 * np.pi * df['DayOfWeek'] / 7)
    df['DayOfWeek_Cos'] = np.cos(2 * np.pi * df['DayOfWeek'] / 7)
    
    print(f"   ✓ Created 20 time-based features")
    
    return df

# Apply to both datasets
train = create_time_features(train, "Training Data")
test = create_time_features(test, "Test Data")

# ============================================================================
# PART 2: FEATURE SUMMARY
# ============================================================================

print("\n" + "="*80)
print("[3] Feature Summary")
print("="*80)

new_time_features = [
    'Year', 'Month', 'Day', 'Quarter', 'DayOfWeek', 'WeekOfYear',
    'Is_Weekend', 'Is_Month_Start', 'Is_Month_End', 
    'Is_Quarter_Start', 'Is_Quarter_End', 'Is_Year_Start', 'Is_Year_End',
    'Month_Sin', 'Month_Cos', 'Week_Sin', 'Week_Cos', 
    'DayOfWeek_Sin', 'DayOfWeek_Cos'
]

print(f"\n📊 Time Features Created (20 total):")
print("-" * 80)

print("\n   Basic Time Components (6):")
print("   1. Year          - Year (2010, 2011, 2012)")
print("   2. Month         - Month of year (1-12)")
print("   3. Day           - Day of month (1-31)")
print("   4. Quarter       - Quarter of year (1-4)")
print("   5. DayOfWeek     - Day of week (0=Mon, 6=Sun)")
print("   6. WeekOfYear    - Week of year (1-52)")

print("\n   Binary Indicators (7):")
print("   7. Is_Weekend         - Weekend flag (0/1)")
print("   8. Is_Month_Start     - First day of month (0/1)")
print("   9. Is_Month_End       - Last day of month (0/1)")
print("   10. Is_Quarter_Start  - First day of quarter (0/1)")
print("   11. Is_Quarter_End    - Last day of quarter (0/1)")
print("   12. Is_Year_Start     - First day of year (0/1)")
print("   13. Is_Year_End       - Last day of year (0/1)")

print("\n   Cyclical Features (6):")
print("   14. Month_Sin         - Month sine transform")
print("   15. Month_Cos         - Month cosine transform")
print("   16. Week_Sin          - Week sine transform")
print("   17. Week_Cos          - Week cosine transform")
print("   18. DayOfWeek_Sin     - Day of week sine transform")
print("   19. DayOfWeek_Cos     - Day of week cosine transform")

print("\n💡 Why Cyclical Features?")
print("   - Capture cyclical nature of time (Dec → Jan continuity)")
print("   - Help ML models understand time is circular, not linear")
print("   - Improves seasonal pattern recognition")

# ============================================================================
# PART 3: VERIFY FEATURES
# ============================================================================

print("\n" + "="*80)
print("[4] Verifying Features")
print("="*80)

print("\n📋 Sample Data (Train - First 5 rows):")
sample_cols = ['Date', 'Year', 'Month', 'Quarter', 'DayOfWeek', 'Is_Weekend', 'WeekOfYear', 'Weekly_Sales']
print(train[sample_cols].head().to_string(index=False))

print("\n📊 Feature Statistics (Training Data):")
print("-" * 80)

print(f"\n   Year Distribution:")
year_counts = train['Year'].value_counts().sort_index()
for year, count in year_counts.items():
    print(f"      {year}: {count:,} records ({count/len(train)*100:.1f}%)")

print(f"\n   Quarter Distribution:")
quarter_counts = train['Quarter'].value_counts().sort_index()
for quarter, count in quarter_counts.items():
    print(f"      Q{quarter}: {count:,} records ({count/len(train)*100:.1f}%)")

print(f"\n   Weekend vs Weekday:")
print(f"      Weekday: {(train['Is_Weekend'] == 0).sum():,} records ({(train['Is_Weekend'] == 0).sum()/len(train)*100:.1f}%)")
print(f"      Weekend: {(train['Is_Weekend'] == 1).sum():,} records ({(train['Is_Weekend'] == 1).sum()/len(train)*100:.1f}%)")

print(f"\n   Month Start/End:")
print(f"      Month Start: {train['Is_Month_Start'].sum():,} records")
print(f"      Month End:   {train['Is_Month_End'].sum():,} records")

# ============================================================================
# PART 4: CONSISTENCY CHECK
# ============================================================================

print("\n" + "="*80)
print("[5] Train-Test Consistency Check")
print("="*80)

train_cols = set(train.columns)
test_cols = set(test.columns)

common_cols = train_cols.intersection(test_cols)
train_only = train_cols - test_cols
test_only = test_cols - train_cols

print(f"\n   Common columns: {len(common_cols)}")
print(f"   Train-only: {list(train_only) if train_only else 'None'}")
print(f"   Test-only: {list(test_only) if test_only else 'None'}")

if train_only == {'Weekly_Sales'} and len(test_only) == 0:
    print("\n   ✅ PERFECT: Test has all features except target variable")
else:
    print("\n   ⚠ WARNING: Unexpected column differences!")

print(f"\n   Final Column Count:")
print(f"   - Train: {len(train.columns)} columns")
print(f"   - Test:  {len(test.columns)} columns")

# ============================================================================
# PART 5: SAVE PROCESSED DATA
# ============================================================================

print("\n" + "="*80)
print("[6] Saving Data with Time Features")
print("="*80)

output_dir = 'processed_data/Stage1.3.1'
os.makedirs(output_dir, exist_ok=True)

train_output = os.path.join(output_dir, 'train_time_features.csv')
test_output = os.path.join(output_dir, 'test_time_features.csv')

train.to_csv(train_output, index=False)
test.to_csv(test_output, index=False)

train_size = os.path.getsize(train_output) / (1024 * 1024)
test_size = os.path.getsize(test_output) / (1024 * 1024)

print(f"\n💾 Saved Training Data:")
print(f"   File: {train_output}")
print(f"   Size: {train_size:.2f} MB")
print(f"   Rows: {len(train):,}")
print(f"   Columns: {len(train.columns)} (added {len(new_time_features)} features)")

print(f"\n💾 Saved Test Data:")
print(f"   File: {test_output}")
print(f"   Size: {test_size:.2f} MB")
print(f"   Rows: {len(test):,}")
print(f"   Columns: {len(test.columns)} (added {len(new_time_features)} features)")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ STEP 1.3.1 COMPLETED SUCCESSFULLY!")
print("="*80)

print(f"""
📊 Summary:

   Time Features Created: 20
   ├─ Basic Components: 6 (Year, Month, Day, Quarter, DayOfWeek, WeekOfYear)
   ├─ Binary Indicators: 7 (Weekend, Month/Quarter/Year Start/End)
   └─ Cyclical Features: 6 (Sin/Cos transforms for Month, Week, DayOfWeek)

   Training Data:
   ├─ Before: {train.shape[0]:,} rows × {train.shape[1] - len(new_time_features)} columns
   ├─ After:  {train.shape[0]:,} rows × {train.shape[1]} columns
   └─ Added:  20 time-based features

   Test Data:
   ├─ Before: {test.shape[0]:,} rows × {test.shape[1] - len(new_time_features)} columns
   ├─ After:  {test.shape[0]:,} rows × {test.shape[1]} columns
   └─ Added:  20 time-based features

✅ Actions Completed:
   1. Created 6 basic time components
   2. Created 7 binary time indicators
   3. Created 6 cyclical features (sine/cosine transforms)
   4. Applied to BOTH train and test datasets
   5. Verified train-test consistency
   6. Saved processed datasets

📁 Output Files:
   - {train_output}
   - {test_output}

🔍 Why These Features Matter (from EDA):
   - Seasonality is DOMINANT (Q4 = 35-40% higher than Q1)
   - Monthly patterns clear (Nov-Dec peak)
   - Weekly patterns exist
   - These features will help capture seasonal variations

🔜 Next Step:
   Step 1.3.2: Create Lag Features (previous weeks' sales)
""")

print("="*80)

