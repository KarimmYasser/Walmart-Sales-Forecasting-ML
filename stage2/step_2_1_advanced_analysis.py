"""
============================================================================
Milestone 2 - Task 2.1: Advanced Data Analysis
============================================================================
This script performs:
1. Time Series Analysis (trend, seasonality, cyclic patterns)
2. Statistical Tests (ADF test for stationarity)
3. Correlation Analysis (features vs sales)

Input: processed_data/Final/train_final.csv
Output: outputs/analysis_results/
============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

print("MILESTONE 2 - TASK 2.1: ADVANCED DATA ANALYSIS")

# Determine correct path to Stage 1 output (works from stage2/ or project root)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
stage1_output = os.path.join(project_root, 'stage1', 'processed_data', 'Stage1.3.4_Final')

# Load data and create output directories
train_path = os.path.join(stage1_output, 'train_final.csv')
print(f"\nLoading data from: {train_path}")
train = pd.read_csv(train_path)    
train['Date'] = pd.to_datetime(train['Date'])
train = train.sort_values(['Store', 'Dept', 'Date']).reset_index(drop=True)

# Create output directories relative to script location
output_base = os.path.join(script_dir, 'outputs')
os.makedirs(os.path.join(output_base, 'analysis_results'), exist_ok=True)
os.makedirs(os.path.join(output_base, 'visualizations'), exist_ok=True)
print(f"Output directory: {output_base}\n")

# ============================================================================
# 2. TIME SERIES DECOMPOSITION
# ============================================================================
print("\n[1/4] Time series decomposition...")

# Aggregate to weekly total sales for easier analysis
weekly_sales = train.groupby('Date')['Weekly_Sales'].sum().reset_index()
weekly_sales = weekly_sales.set_index('Date').sort_index()

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
save_path = os.path.join(output_base, 'visualizations', '01_time_series_decomposition.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 3. STATIONARITY TEST (Augmented Dickey-Fuller Test)
# ============================================================================
print("[2/4] Stationarity testing...")

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

# Save ADF results
adf_path = os.path.join(output_base, 'analysis_results', 'adf_test_results.json')
with open(adf_path, 'w') as f:
    json.dump(adf_results, f, indent=4)

# ============================================================================
# 4. CORRELATION ANALYSIS
# ============================================================================
print("[3/4] Correlation analysis...")

# Select numerical features for correlation analysis
numerical_features = [
    'Weekly_Sales', 'Temperature', 'Fuel_Price', 'CPI', 'Unemployment',
    'Size', 'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5',
    'Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4',
    'Sales_Rolling_Mean_4', 'Sales_Rolling_Mean_8', 'Sales_Rolling_Std_4'
]

# Filter available columns and calculate correlation matrix
available_features = [col for col in numerical_features if col in train.columns]
correlation_data = train[available_features].copy()
corr_matrix = correlation_data.corr()

# Save correlation results
corr_path = os.path.join(output_base, 'analysis_results', 'correlation_matrix.csv')
sales_corr_path = os.path.join(output_base, 'analysis_results', 'sales_correlations.csv')
corr_matrix.to_csv(corr_path)
sales_correlations = corr_matrix['Weekly_Sales'].sort_values(ascending=False)
sales_correlations.to_csv(sales_corr_path)

# Visualize correlation heatmap (top features only)
top_features = ['Weekly_Sales'] + list(sales_correlations.drop('Weekly_Sales').abs().nlargest(10).index)
top_corr = correlation_data[top_features].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(top_corr, annot=True, fmt='.3f', cmap='RdBu_r', center=0, 
            square=True, linewidths=1, cbar_kws={"shrink": 0.8})
plt.title('Correlation Heatmap - Top Features vs Weekly Sales', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
save_path = os.path.join(output_base, 'visualizations', '02_correlation_heatmap.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 5. HOLIDAY vs NON-HOLIDAY ANALYSIS
# ============================================================================
print("[4/4] Holiday impact analysis...")

holiday_stats = train.groupby('IsHoliday')['Weekly_Sales'].agg([
    ('count', 'count'),
    ('mean', 'mean'),
    ('median', 'median'),
    ('std', 'std'),
    ('min', 'min'),
    ('max', 'max')
]).round(2)

holiday_path = os.path.join(output_base, 'analysis_results', 'holiday_impact_stats.csv')
holiday_stats.to_csv(holiday_path)

# Calculate percentage difference
non_holiday_mean = holiday_stats.loc[False, 'mean']
holiday_mean = holiday_stats.loc[True, 'mean']
pct_increase = ((holiday_mean - non_holiday_mean) / non_holiday_mean) * 100

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
save_path = os.path.join(output_base, 'visualizations', '03_holiday_impact.png')
plt.savefig(save_path, dpi=300, bbox_inches='tight')
plt.close()

print("\nTASK 2.1 COMPLETE - Advanced Data Analysis")

