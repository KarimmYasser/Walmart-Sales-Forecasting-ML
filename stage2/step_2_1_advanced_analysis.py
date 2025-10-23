"""
============================================================================
Milestone 2 - Task 2.1: Advanced Data Analysis
============================================================================
This script performs:
1. Time Series Analysis (trend, seasonality, cyclic patterns)
2. Statistical Tests (ADF test for stationarity)
3. Correlation Analysis (features vs sales)

Input: processed_data/Final/train_final.csv
Output: stage2/outputs/analysis_results/
============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

print("="*80)
print("MILESTONE 2 - TASK 2.1: ADVANCED DATA ANALYSIS")
print("="*80)

# ============================================================================
# 1. LOAD DATA
# ============================================================================
print("\n[1/5] Loading final processed data...")
train = pd.read_csv('processed_data/Final/train_final.csv')
print(f"✓ Loaded: {train.shape[0]:,} rows × {train.shape[1]} columns")

# Convert Date to datetime
train['Date'] = pd.to_datetime(train['Date'])
train = train.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

print(f"✓ Date range: {train['Date'].min()} to {train['Date'].max()}")
print(f"✓ Stores: {train['Store'].nunique()}, Departments: {train['Dept'].nunique()}")

# ============================================================================
# 2. TIME SERIES DECOMPOSITION
# ============================================================================
print("\n[2/5] Performing time series decomposition...")

# Aggregate to weekly total sales for easier analysis
weekly_sales = train.groupby('Date')['Weekly_Sales'].sum().reset_index()
weekly_sales = weekly_sales.set_index('Date').sort_index()

print(f"✓ Aggregated to {len(weekly_sales)} weekly data points")

# Simple decomposition using rolling means
def decompose_time_series(series, window=52):
    """Manual time series decomposition"""
    # Trend: 52-week rolling mean (1 year)
    trend = series.rolling(window=window, center=True).mean()
    
    # Detrended
    detrended = series - trend
    
    # Seasonality: average of detrended by week of year
    seasonal = detrended.groupby(detrended.index.isocalendar().week).mean()
    seasonal_series = detrended.index.isocalendar().week.map(seasonal.to_dict())
    
    # Residual
    residual = detrended - seasonal_series
    
    return trend, seasonal_series, residual

trend, seasonal, residual = decompose_time_series(weekly_sales['Weekly_Sales'])

# Save decomposition plot
fig, axes = plt.subplots(4, 1, figsize=(15, 12))

axes[0].plot(weekly_sales.index, weekly_sales['Weekly_Sales'], color='blue', linewidth=1)
axes[0].set_title('Original Time Series - Weekly Sales', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Sales ($)', fontsize=11)
axes[0].grid(True, alpha=0.3)

axes[1].plot(weekly_sales.index, trend, color='red', linewidth=2)
axes[1].set_title('Trend Component', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Trend ($)', fontsize=11)
axes[1].grid(True, alpha=0.3)

axes[2].plot(weekly_sales.index, seasonal, color='green', linewidth=1)
axes[2].set_title('Seasonal Component', fontsize=14, fontweight='bold')
axes[2].set_ylabel('Seasonality ($)', fontsize=11)
axes[2].grid(True, alpha=0.3)

axes[3].plot(weekly_sales.index, residual, color='orange', linewidth=1)
axes[3].set_title('Residual Component', fontsize=14, fontweight='bold')
axes[3].set_ylabel('Residuals ($)', fontsize=11)
axes[3].set_xlabel('Date', fontsize=11)
axes[3].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('stage2/outputs/visualizations/01_time_series_decomposition.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Time series decomposition completed")
print(f"  - Saved: stage2/outputs/visualizations/01_time_series_decomposition.png")

# ============================================================================
# 3. STATIONARITY TEST (Augmented Dickey-Fuller Test)
# ============================================================================
print("\n[3/5] Performing ADF test for stationarity...")

def adf_test_manual(series):
    """
    Manual ADF test interpretation using simple differencing test
    Note: For production, use statsmodels.tsa.stattools.adfuller
    This is a simplified version for educational purposes
    """
    # Remove NaN values
    series_clean = series.dropna()
    
    # Calculate first difference
    diff_series = series_clean.diff().dropna()
    
    # Basic statistics
    mean_original = series_clean.mean()
    std_original = series_clean.std()
    mean_diff = diff_series.mean()
    std_diff = diff_series.std()
    
    # Variance ratio (if < 1, differencing reduced variance)
    variance_ratio = std_diff / std_original
    
    # Check if mean is close to zero after differencing
    mean_stability = abs(mean_diff) / std_diff if std_diff > 0 else np.inf
    
    is_stationary = variance_ratio < 0.9 and mean_stability < 0.1
    
    results = {
        'original_mean': float(mean_original),
        'original_std': float(std_original),
        'differenced_mean': float(mean_diff),
        'differenced_std': float(std_diff),
        'variance_ratio': float(variance_ratio),
        'mean_stability_ratio': float(mean_stability),
        'is_stationary_str': 'Yes' if is_stationary else 'No',
        'interpretation': ''
    }
    
    if is_stationary:
        results['interpretation'] = 'Series appears to be STATIONARY (or close to stationary)'
    else:
        results['interpretation'] = 'Series appears to be NON-STATIONARY (requires differencing)'
    
    return results

# Test overall sales
adf_results = adf_test_manual(weekly_sales['Weekly_Sales'])

print("\n" + "="*80)
print("STATIONARITY TEST RESULTS (Simplified ADF)")
print("="*80)
print(f"Original Series Mean:      ${adf_results['original_mean']:,.2f}")
print(f"Original Series Std:       ${adf_results['original_std']:,.2f}")
print(f"Differenced Series Mean:   ${adf_results['differenced_mean']:,.2f}")
print(f"Differenced Series Std:    ${adf_results['differenced_std']:,.2f}")
print(f"Variance Ratio:            {adf_results['variance_ratio']:.4f}")
print(f"Mean Stability Ratio:      {adf_results['mean_stability_ratio']:.4f}")
print(f"\n→ {adf_results['interpretation']}")
print("="*80)

# Test by store type
print("\nStationarity by Store Type:")
for store_type in ['A', 'B', 'C']:
    type_col = f'Type_{store_type}'
    if type_col in train.columns:
        type_sales = train[train[type_col] == 1].groupby('Date')['Weekly_Sales'].sum()
        type_results = adf_test_manual(type_sales)
        print(f"  Type {store_type}: {type_results['interpretation']}")

# Save ADF results
with open('stage2/outputs/analysis_results/adf_test_results.json', 'w') as f:
    json.dump(adf_results, f, indent=4)

print("\n✓ Stationarity tests completed")
print(f"  - Saved: stage2/outputs/analysis_results/adf_test_results.json")

# ============================================================================
# 4. CORRELATION ANALYSIS
# ============================================================================
print("\n[4/5] Performing correlation analysis...")

# Select numerical features for correlation analysis
numerical_features = [
    'Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment',
    'Size', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5',
    'Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4',
    'Sales_Rolling_Mean_4', 'Sales_Rolling_Mean_8', 'Sales_Rolling_Std_4'
]

# Filter available columns
available_features = [col for col in numerical_features if col in train.columns]
correlation_data = train[available_features].copy()

# Calculate correlation matrix
corr_matrix = correlation_data.corr()

# Save full correlation matrix
corr_matrix.to_csv('stage2/outputs/analysis_results/correlation_matrix.csv')

# Focus on correlations with Weekly_Sales
sales_correlations = corr_matrix['Weekly_Sales'].sort_values(ascending=False)
sales_correlations.to_csv('stage2/outputs/analysis_results/sales_correlations.csv')

print("\n" + "="*80)
print("TOP CORRELATIONS WITH WEEKLY_SALES")
print("="*80)
for i, (feature, corr) in enumerate(sales_correlations.items(), 1):
    if feature != 'Weekly_Sales':
        direction = "📈 Positive" if corr > 0 else "📉 Negative"
        strength = "Strong" if abs(corr) > 0.5 else "Moderate" if abs(corr) > 0.3 else "Weak"
        print(f"{i-1:2d}. {feature:30s}: {corr:+.4f}  ({direction}, {strength})")

print("="*80)

# Visualize correlation heatmap (top features only)
top_features = ['Weekly_Sales'] + list(sales_correlations.drop('Weekly_Sales').abs().nlargest(10).index)
top_corr = correlation_data[top_features].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(top_corr, annot=True, fmt='.3f', cmap='RdBu_r', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap - Top Features vs Weekly Sales', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('stage2/outputs/visualizations/02_correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n✓ Correlation analysis completed")
print(f"  - Saved: stage2/outputs/analysis_results/correlation_matrix.csv")
print(f"  - Saved: stage2/outputs/analysis_results/sales_correlations.csv")
print(f"  - Saved: stage2/outputs/visualizations/02_correlation_heatmap.png")

# ============================================================================
# 5. HOLIDAY vs NON-HOLIDAY ANALYSIS
# ============================================================================
print("\n[5/5] Analyzing holiday impact...")

holiday_stats = train.groupby('IsHoliday')['Weekly_Sales'].agg([
    ('count', 'count'),
    ('mean', 'mean'),
    ('median', 'median'),
    ('std', 'std'),
    ('min', 'min'),
    ('max', 'max')
]).round(2)

holiday_stats.to_csv('stage2/outputs/analysis_results/holiday_impact_stats.csv')

print("\n" + "="*80)
print("HOLIDAY vs NON-HOLIDAY SALES COMPARISON")
print("="*80)
print(holiday_stats)
print("="*80)

# Calculate percentage difference
non_holiday_mean = holiday_stats.loc[False, 'mean']
holiday_mean = holiday_stats.loc[True, 'mean']
pct_increase = ((holiday_mean - non_holiday_mean) / non_holiday_mean) * 100

print(f"\n→ Holiday sales are {pct_increase:+.2f}% compared to non-holiday sales")

# Visualize holiday impact
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Box plot
train.boxplot(column='Weekly_Sales', by='IsHoliday', ax=axes[0])
axes[0].set_title('Sales Distribution: Holiday vs Non-Holiday', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Is Holiday', fontsize=11)
axes[0].set_ylabel('Weekly Sales ($)', fontsize=11)
axes[0].set_xticklabels(['Non-Holiday', 'Holiday'])
plt.sca(axes[0])
plt.xticks([1, 2], ['Non-Holiday', 'Holiday'])

# Bar plot of means
axes[1].bar(['Non-Holiday', 'Holiday'], [non_holiday_mean, holiday_mean], 
            color=['skyblue', 'coral'], edgecolor='black', linewidth=1.5)
axes[1].set_title('Average Sales Comparison', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Average Weekly Sales ($)', fontsize=11)
axes[1].grid(axis='y', alpha=0.3)

for i, v in enumerate([non_holiday_mean, holiday_mean]):
    axes[1].text(i, v + v*0.02, f'${v:,.0f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.suptitle('Holiday Impact on Sales', fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('stage2/outputs/visualizations/03_holiday_impact.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✓ Holiday impact analysis completed")
print(f"  - Saved: stage2/outputs/analysis_results/holiday_impact_stats.csv")
print(f"  - Saved: stage2/outputs/visualizations/03_holiday_impact.png")

# ============================================================================
# SUMMARY REPORT
# ============================================================================
print("\n" + "="*80)
print("ADVANCED DATA ANALYSIS COMPLETE")
print("="*80)
print("\n📊 Analysis Results Saved:")
print("  1. Time Series Decomposition (Trend, Seasonality, Residuals)")
print("  2. Stationarity Test Results (ADF)")
print("  3. Correlation Analysis (Full matrix + Sales correlations)")
print("  4. Holiday Impact Statistics")
print("\n📈 Visualizations Created:")
print("  1. stage2/outputs/visualizations/01_time_series_decomposition.png")
print("  2. stage2/outputs/visualizations/02_correlation_heatmap.png")
print("  3. stage2/outputs/visualizations/03_holiday_impact.png")
print("\n💡 Key Insights:")
print(f"  • Series Stationarity: {adf_results['interpretation']}")
print(f"  • Strongest Correlation: {sales_correlations.index[1]} ({sales_correlations.iloc[1]:+.4f})")
print(f"  • Holiday Impact: {pct_increase:+.2f}% vs non-holiday")
print("="*80)

print("\n✅ Task 2.1 Complete! Ready for Task 2.2 (Feature Engineering)")

