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
Output: stage2/outputs/enhanced_features/
============================================================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("MILESTONE 2 - TASK 2.2: ENHANCED FEATURE ENGINEERING")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1/8] Loading processed data...")
train = pd.read_csv('processed_data/Final/train_final.csv')
test = pd.read_csv('processed_data/Final/test_final.csv')

# Convert Date to datetime
train['Date'] = pd.to_datetime(train['Date'])
test['Date'] = pd.to_datetime(test['Date'])

# Sort by Store, Dept, Date
train = train.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)
test = test.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

print(f"✓ Train: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"✓ Test: {test.shape[0]:,} rows × {test.shape[1]} columns")

# ============================================================================
# 2. ADVANCED ROLLING STATISTICS
# ============================================================================
print("\n[2/8] Creating advanced rolling statistics...")

def create_advanced_rolling_features(df, has_sales=True):
    """Create advanced rolling window features"""
    df_copy = df.copy()
    
    if has_sales:
        # Exponential Moving Averages (EMA)
        df_copy['Sales_EMA_4'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.ewm(span=4, adjust=False).mean()
        )
        df_copy['Sales_EMA_8'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.ewm(span=8, adjust=False).mean()
        )
        df_copy['Sales_EMA_12'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.ewm(span=12, adjust=False).mean()
        )
        
        # Rolling Min/Max (4-week windows)
        df_copy['Sales_Rolling_Min_4'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).min()
        )
        df_copy['Sales_Rolling_Max_4'] = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).max()
        )
        
        # Rolling Range
        df_copy['Sales_Rolling_Range_4'] = df_copy['Sales_Rolling_Max_4'] - df_copy['Sales_Rolling_Min_4']
        
        # Sales Trend (difference between EMA_4 and EMA_12)
        df_copy['Sales_Trend'] = df_copy['Sales_EMA_4'] - df_copy['Sales_EMA_12']
        
        # Rolling Coefficient of Variation (CV = std/mean)
        rolling_mean = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).mean()
        )
        rolling_std = df_copy.groupby(['Store', 'Dept'])['Weekly_Sales'].transform(
            lambda x: x.rolling(window=4, min_periods=1).std()
        )
        df_copy['Sales_CV_4'] = rolling_std / (rolling_mean + 1)  # +1 to avoid division by zero
        
        # Sales Acceleration (second derivative)
        df_copy['Sales_Acceleration'] = df_copy.groupby(['Store', 'Dept'])['Sales_Momentum'].transform(
            lambda x: x.diff()
        )
        
        print(f"  ✓ Created 10 advanced rolling features for {'train' if has_sales else 'test'}")
    
    return df_copy

train = create_advanced_rolling_features(train, has_sales=True)
test = create_advanced_rolling_features(test, has_sales=False)

# ============================================================================
# 3. SEASONAL FEATURES
# ============================================================================
print("\n[3/8] Creating seasonal features...")

def create_seasonal_features(df):
    """Create seasonal and holiday-related features"""
    df_copy = df.copy()
    
    # Season (Meteorological)
    df_copy['Season'] = df_copy['Month'].apply(lambda x: 
        'Winter' if x in [12, 1, 2] else
        'Spring' if x in [3, 4, 5] else
        'Summer' if x in [6, 7, 8] else
        'Fall'
    )
    
    # Holiday Season (Nov-Dec for Black Friday, Christmas)
    df_copy['Is_Holiday_Season'] = ((df_copy['Month'] == 11) | (df_copy['Month'] == 12)).astype(int)
    
    # Back to School Season (July-August)
    df_copy['Is_BackToSchool_Season'] = ((df_copy['Month'] == 7) | (df_copy['Month'] == 8)).astype(int)
    
    # Super Bowl (typically early February)
    df_copy['Is_SuperBowl_Week'] = ((df_copy['Month'] == 2) & (df_copy['Day'] <= 14)).astype(int)
    
    # Days Until/Since Major Holidays (approximate)
    # Thanksgiving (4th Thursday of November)
    df_copy['Days_To_Thanksgiving'] = df_copy.apply(lambda row: 
        (pd.Timestamp(f"{row['Year']}-11-24") - row['Date']).days if row['Month'] <= 11 
        else (pd.Timestamp(f"{row['Year']+1}-11-24") - row['Date']).days, axis=1
    )
    
    # Christmas
    df_copy['Days_To_Christmas'] = df_copy.apply(lambda row: 
        (pd.Timestamp(f"{row['Year']}-12-25") - row['Date']).days if row['Month'] <= 12 
        else (pd.Timestamp(f"{row['Year']+1}-12-25") - row['Date']).days, axis=1
    )
    
    # Encode Season
    df_copy['Season_Winter'] = (df_copy['Season'] == 'Winter').astype(int)
    df_copy['Season_Spring'] = (df_copy['Season'] == 'Spring').astype(int)
    df_copy['Season_Summer'] = (df_copy['Season'] == 'Summer').astype(int)
    df_copy['Season_Fall'] = (df_copy['Season'] == 'Fall').astype(int)
    
    # Drop original Season column
    df_copy = df_copy.drop('Season', axis=1)
    
    print(f"  ✓ Created 10 seasonal features")
    
    return df_copy

train = create_seasonal_features(train)
test = create_seasonal_features(test)

# ============================================================================
# 4. STORE PERFORMANCE FEATURES
# ============================================================================
print("\n[4/8] Creating store performance features...")

# Calculate store-level statistics from training data
store_stats = train.groupby('Store')['Weekly_Sales'].agg([
    ('Store_Avg_Sales', 'mean'),
    ('Store_Std_Sales', 'std'),
    ('Store_Min_Sales', 'min'),
    ('Store_Max_Sales', 'max')
]).reset_index()

# Department-level statistics
dept_stats = train.groupby('Dept')['Weekly_Sales'].agg([
    ('Dept_Avg_Sales', 'mean'),
    ('Dept_Std_Sales', 'std')
]).reset_index()

# Store-Department combination statistics
store_dept_stats = train.groupby(['Store', 'Dept'])['Weekly_Sales'].agg([
    ('StoreDept_Avg_Sales', 'mean'),
    ('StoreDept_Std_Sales', 'std')
]).reset_index()

# Merge statistics to both train and test
train = train.merge(store_stats, on='Store', how='left')
train = train.merge(dept_stats, on='Dept', how='left')
train = train.merge(store_dept_stats, on=['Store', 'Dept'], how='left')

test = test.merge(store_stats, on='Store', how='left')
test = test.merge(dept_stats, on='Dept', how='left')
test = test.merge(store_dept_stats, on=['Store', 'Dept'], how='left')

# Sales deviation from store average (only for train)
if 'Weekly_Sales' in train.columns:
    train['Sales_Deviation_From_Store_Avg'] = train['Weekly_Sales'] - train['Store_Avg_Sales']
    train['Sales_Deviation_From_Dept_Avg'] = train['Weekly_Sales'] - train['Dept_Avg_Sales']
    train['Sales_Deviation_From_StoreDept_Avg'] = train['Weekly_Sales'] - train['StoreDept_Avg_Sales']

print(f"  ✓ Created 6 store performance features for train")
print(f"  ✓ Created 6 store performance features for test")

# ============================================================================
# 5. PROMOTIONAL INTENSITY METRICS
# ============================================================================
print("\n[5/8] Creating promotional intensity metrics...")

def create_promo_features(df):
    """Create promotional intensity features"""
    df_copy = df.copy()
    
    # Total markdown amount
    markdown_cols = ['MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5']
    df_copy['Total_MarkDown'] = df_copy[markdown_cols].sum(axis=1)
    
    # Number of active markdowns
    has_markdown_cols = [f'Has_{col}' for col in markdown_cols]
    if all(col in df_copy.columns for col in has_markdown_cols):
        df_copy['Num_Active_MarkDowns'] = df_copy[has_markdown_cols].sum(axis=1)
    
    # Promotion Intensity (Total markdown / Store Size)
    df_copy['Promo_Intensity'] = df_copy['Total_MarkDown'] / (df_copy['Size'] + 1)
    
    # Rolling average of promotions (4-week window)
    df_copy['Total_MarkDown_Rolling_4'] = df_copy.groupby(['Store', 'Dept'])['Total_MarkDown'].transform(
        lambda x: x.rolling(window=4, min_periods=1).mean()
    )
    
    print(f"  ✓ Created 4 promotional intensity features")
    
    return df_copy

train = create_promo_features(train)
test = create_promo_features(test)

# ============================================================================
# 6. ECONOMIC INDICATOR INTERACTIONS
# ============================================================================
print("\n[6/8] Creating economic indicator interactions...")

def create_economic_interactions(df):
    """Create interaction features between economic indicators"""
    df_copy = df.copy()
    
    # CPI × Unemployment (economic stress indicator)
    df_copy['Economic_Stress'] = df_copy['CPI'] * df_copy['Unemployment']
    
    # Temperature × IsHoliday (holiday weather effect)
    df_copy['Holiday_Temperature'] = df_copy['Temperature'] * df_copy['IsHoliday']
    
    # Fuel_Price × Unemployment (consumer spending power)
    df_copy['Spending_Power'] = df_copy['Fuel_Price'] * df_copy['Unemployment']
    
    # Store Size × CPI (store purchasing power)
    df_copy['Store_Purchasing_Power'] = df_copy['Size'] * df_copy['CPI']
    
    print(f"  ✓ Created 4 economic interaction features")
    
    return df_copy

train = create_economic_interactions(train)
test = create_economic_interactions(test)

# ============================================================================
# 7. TIME-BASED AGGREGATIONS
# ============================================================================
print("\n[7/8] Creating time-based aggregation features...")

def create_time_aggregations(df, has_sales=True):
    """Create monthly and quarterly aggregations"""
    df_copy = df.copy()
    
    if has_sales:
        # Monthly sales statistics per store
        df_copy['Month_Store_Avg_Sales'] = df_copy.groupby(['Store', 'Year', 'Month'])['Weekly_Sales'].transform('mean')
        df_copy['Month_Store_Total_Sales'] = df_copy.groupby(['Store', 'Year', 'Month'])['Weekly_Sales'].transform('sum')
        
        # Quarterly sales statistics per store
        df_copy['Quarter_Store_Avg_Sales'] = df_copy.groupby(['Store', 'Year', 'Quarter'])['Weekly_Sales'].transform('mean')
        df_copy['Quarter_Store_Total_Sales'] = df_copy.groupby(['Store', 'Year', 'Quarter'])['Weekly_Sales'].transform('sum')
        
        # Year-over-Year growth (if data available)
        df_copy['Store_Sales_YoY_Growth'] = df_copy.groupby(['Store', 'Month', 'Day'])['Weekly_Sales'].transform(
            lambda x: x.pct_change(periods=1)
        )
        
        print(f"  ✓ Created 5 time aggregation features for {'train' if has_sales else 'test'}")
    
    return df_copy

train = create_time_aggregations(train, has_sales=True)
test = create_time_aggregations(test, has_sales=False)

# ============================================================================
# 8. SAVE ENHANCED DATASETS
# ============================================================================
print("\n[8/8] Saving enhanced datasets...")

# Save to stage2 outputs
train.to_csv('stage2/outputs/enhanced_features/train_enhanced.csv', index=False)
test.to_csv('stage2/outputs/enhanced_features/test_enhanced.csv', index=False)

print(f"✓ Saved: stage2/outputs/enhanced_features/train_enhanced.csv")
print(f"  - Shape: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"✓ Saved: stage2/outputs/enhanced_features/test_enhanced.csv")
print(f"  - Shape: {test.shape[0]:,} rows × {test.shape[1]} columns")

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

with open('stage2/outputs/enhanced_features/feature_summary.json', 'w') as f:
    json.dump(feature_summary, f, indent=4, default=str)

print("\n✓ Saved: stage2/outputs/enhanced_features/feature_summary.json")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("ENHANCED FEATURE ENGINEERING COMPLETE")
print("="*80)
print(f"\n📊 Feature Summary:")
print(f"  • Original Features (Milestone 1): 49")
print(f"  • New Features Added: {feature_summary['total_new_features']}")
print(f"  • Total Features Now: {train.shape[1]}")
print(f"\n📁 Feature Categories:")
for category, features in new_features.items():
    print(f"  • {category}: {len(features)} features")
print(f"\n💾 Output Files:")
print(f"  • train_enhanced.csv: {train.shape[0]:,} rows × {train.shape[1]} columns")
print(f"  • test_enhanced.csv: {test.shape[0]:,} rows × {test.shape[1]} columns")
print(f"  • feature_summary.json")
print("="*80)

print("\n✅ Task 2.2 Complete! Ready for Task 2.3 (Advanced Visualizations)")

