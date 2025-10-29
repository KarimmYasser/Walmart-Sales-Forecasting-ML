"""
============================================================================
Milestone 2 - Task 2.3: Advanced Visualizations
============================================================================
This script creates advanced visualizations:
1. Historical trends with forecasting patterns
2. Seasonal decomposition visualizations
3. Store performance comparisons
4. Department performance heatmaps
5. Promotional effectiveness analysis
6. External factor impact visualizations
7. Interactive dashboard-style reports

Input: outputs/enhanced_features/train_enhanced.csv
Output: outputs/visualizations/
============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("MILESTONE 2 - TASK 2.3: ADVANCED VISUALIZATIONS")
print("="*80)

# Load data and create output directory
train = pd.read_csv('outputs/enhanced_features/train_enhanced.csv')
train['Date'] = pd.to_datetime(train['Date'])
train = train.sort_values('Date').reset_index(drop=True)
os.makedirs('outputs/visualizations', exist_ok=True)

# Historical Trends with EMA
print("\n[1/7] Historical trends...")

weekly_sales = train.groupby('Date')['Weekly_Sales'].sum().reset_index()

fig, ax = plt.subplots(figsize=(16, 6))

# Plot actual sales
ax.plot(weekly_sales['Date'], weekly_sales['Weekly_Sales'], 
        label='Actual Sales', color='blue', linewidth=1.5, alpha=0.7)

# Plot EMAs (if available in aggregated form)
weekly_ema = train.groupby('Date').agg({
    'Weekly_Sales': 'sum',
    'Sales_EMA_4': 'sum',
    'Sales_EMA_8': 'sum',
    'Sales_EMA_12': 'sum'
}).reset_index()

ax.plot(weekly_ema['Date'], weekly_ema['Sales_EMA_4'], 
        label='4-Week EMA', color='red', linewidth=2, alpha=0.8)
ax.plot(weekly_ema['Date'], weekly_ema['Sales_EMA_8'], 
        label='8-Week EMA', color='green', linewidth=2, alpha=0.8)
ax.plot(weekly_ema['Date'], weekly_ema['Sales_EMA_12'], 
        label='12-Week EMA', color='orange', linewidth=2, alpha=0.8)

ax.set_title('Historical Sales Trends with Exponential Moving Averages', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xlabel('Date', fontsize=12, fontweight='bold')
ax.set_ylabel('Total Weekly Sales ($)', fontsize=12, fontweight='bold')
ax.legend(loc='best', fontsize=11)
ax.grid(True, alpha=0.3)

# Format y-axis
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

plt.tight_layout()
plt.savefig('outputs/visualizations/04_historical_trends_ema.png', dpi=300, bbox_inches='tight')
plt.close()

# Seasonal Patterns
print("[2/7] Seasonal patterns...")

monthly_stats = train.groupby('Month').agg({
    'Weekly_Sales': ['mean', 'sum', 'std'],
    'IsHoliday': 'sum'
}).reset_index()
monthly_stats.columns = ['Month', 'Avg_Sales', 'Total_Sales', 'Std_Sales', 'Holiday_Count']

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Monthly average sales
axes[0, 0].bar(monthly_stats['Month'], monthly_stats['Avg_Sales'], 
               color='steelblue', edgecolor='black', linewidth=1.2)
axes[0, 0].set_title('Average Sales by Month', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Month', fontsize=11)
axes[0, 0].set_ylabel('Average Weekly Sales ($)', fontsize=11)
axes[0, 0].grid(axis='y', alpha=0.3)
axes[0, 0].set_xticks(range(1, 13))
axes[0, 0].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Monthly total sales
axes[0, 1].bar(monthly_stats['Month'], monthly_stats['Total_Sales'], 
               color='coral', edgecolor='black', linewidth=1.2)
axes[0, 1].set_title('Total Sales by Month', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Month', fontsize=11)
axes[0, 1].set_ylabel('Total Weekly Sales ($)', fontsize=11)
axes[0, 1].grid(axis='y', alpha=0.3)
axes[0, 1].set_xticks(range(1, 13))
axes[0, 1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Sales volatility (std)
axes[1, 0].bar(monthly_stats['Month'], monthly_stats['Std_Sales'], 
               color='lightgreen', edgecolor='black', linewidth=1.2)
axes[1, 0].set_title('Sales Volatility by Month (Standard Deviation)', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Month', fontsize=11)
axes[1, 0].set_ylabel('Std Dev of Sales ($)', fontsize=11)
axes[1, 0].grid(axis='y', alpha=0.3)
axes[1, 0].set_xticks(range(1, 13))
axes[1, 0].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

# Holiday count by month
axes[1, 1].bar(monthly_stats['Month'], monthly_stats['Holiday_Count'], 
               color='gold', edgecolor='black', linewidth=1.2)
axes[1, 1].set_title('Holiday Weeks by Month', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Month', fontsize=11)
axes[1, 1].set_ylabel('Number of Holiday Weeks', fontsize=11)
axes[1, 1].grid(axis='y', alpha=0.3)
axes[1, 1].set_xticks(range(1, 13))
axes[1, 1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

plt.suptitle('Seasonal Patterns Analysis', fontsize=18, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('outputs/visualizations/05_seasonal_patterns.png', dpi=300, bbox_inches='tight')
plt.close()

# Store Type Performance
print("[3/7] Store type performance...")

# Determine store type
train['StoreType'] = train.apply(lambda row: 
    'A' if row['Type_A'] == 1 else 'B' if row['Type_B'] == 1 else 'C', axis=1
)

type_stats = train.groupby('StoreType').agg({
    'Weekly_Sales': ['mean', 'sum', 'std', 'count'],
    'Size': 'mean',
    'Total_MarkDown': 'mean'
}).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Average sales by store type
avg_sales = type_stats['Weekly_Sales']['mean']
axes[0].bar(type_stats['StoreType'], avg_sales, 
            color=['#FF6B6B', '#4ECDC4', '#45B7D1'], 
            edgecolor='black', linewidth=1.5)
axes[0].set_title('Average Sales by Store Type', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Store Type', fontsize=11)
axes[0].set_ylabel('Average Weekly Sales ($)', fontsize=11)
axes[0].grid(axis='y', alpha=0.3)

for i, v in enumerate(avg_sales):
    axes[0].text(i, v + v*0.02, f'${v:,.0f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')

# Total sales by store type
total_sales = type_stats['Weekly_Sales']['sum']
axes[1].bar(type_stats['StoreType'], total_sales, 
            color=['#FF6B6B', '#4ECDC4', '#45B7D1'], 
            edgecolor='black', linewidth=1.5)
axes[1].set_title('Total Sales by Store Type', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Store Type', fontsize=11)
axes[1].set_ylabel('Total Sales ($)', fontsize=11)
axes[1].grid(axis='y', alpha=0.3)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))

# Average store size by type
avg_size = type_stats['Size']['mean']
axes[2].bar(type_stats['StoreType'], avg_size, 
            color=['#FF6B6B', '#4ECDC4', '#45B7D1'], 
            edgecolor='black', linewidth=1.5)
axes[2].set_title('Average Store Size by Type', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Store Type', fontsize=11)
axes[2].set_ylabel('Average Size (sq ft)', fontsize=11)
axes[2].grid(axis='y', alpha=0.3)

for i, v in enumerate(avg_size):
    axes[2].text(i, v + v*0.02, f'{v:,.0f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold')

plt.suptitle('Store Type Performance Comparison', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/visualizations/06_store_type_performance.png', dpi=300, bbox_inches='tight')
plt.close()

# Department Performance Heatmap
print("[4/7] Department heatmap...")

# Get top 20 departments by total sales
top_depts = train.groupby('Dept')['Weekly_Sales'].sum().nlargest(20).index

# Create pivot table for heatmap (Department × Month)
dept_month_sales = train[train['Dept'].isin(top_depts)].pivot_table(
    values='Weekly_Sales',
    index='Dept',
    columns='Month',
    aggfunc='mean'
)

plt.figure(figsize=(14, 10))
sns.heatmap(dept_month_sales, cmap='YlOrRd', fmt='.0f', 
            linewidths=0.5, cbar_kws={'label': 'Average Weekly Sales ($)'})
plt.title('Top 20 Departments: Average Sales by Month', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Month', fontsize=12, fontweight='bold')
plt.ylabel('Department', fontsize=12, fontweight='bold')
plt.xticks(range(12), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.savefig('outputs/visualizations/07_department_performance_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# Promotional Effectiveness
print("[5/7] Promotional effectiveness...")

# Compare sales with and without promotions
promo_comparison = train.copy()
promo_comparison['Has_Promo'] = (promo_comparison['Total_MarkDown'] > 0).astype(int)

promo_stats = promo_comparison.groupby('Has_Promo')['Weekly_Sales'].agg([
    ('Mean', 'mean'),
    ('Median', 'median'),
    ('Std', 'std')
]).reset_index()

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Sales distribution comparison
promo_comparison.boxplot(column='Weekly_Sales', by='Has_Promo', ax=axes[0])
axes[0].set_title('Sales Distribution: With vs Without Promotions', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Has Promotion', fontsize=11)
axes[0].set_ylabel('Weekly Sales ($)', fontsize=11)
axes[0].set_xticklabels(['No Promotion', 'With Promotion'])
plt.sca(axes[0])
plt.xticks([1, 2], ['No Promotion', 'With Promotion'])

# Average sales comparison
axes[1].bar(['No Promotion', 'With Promotion'], promo_stats['Mean'], 
            color=['lightblue', 'salmon'], edgecolor='black', linewidth=1.5)
axes[1].set_title('Average Sales Comparison', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Average Weekly Sales ($)', fontsize=11)
axes[1].grid(axis='y', alpha=0.3)

for i, v in enumerate(promo_stats['Mean']):
    axes[1].text(i, v + v*0.02, f'${v:,.0f}', ha='center', va='bottom', 
                fontsize=12, fontweight='bold')

# Promotion impact by store type
promo_by_type = promo_comparison.groupby(['StoreType', 'Has_Promo'])['Weekly_Sales'].mean().unstack()
promo_by_type.plot(kind='bar', ax=axes[2], color=['lightblue', 'salmon'], 
                   edgecolor='black', linewidth=1.2)
axes[2].set_title('Promotion Impact by Store Type', fontsize=14, fontweight='bold')
axes[2].set_xlabel('Store Type', fontsize=11)
axes[2].set_ylabel('Average Weekly Sales ($)', fontsize=11)
axes[2].legend(['No Promotion', 'With Promotion'], loc='best')
axes[2].grid(axis='y', alpha=0.3)
axes[2].set_xticklabels(axes[2].get_xticklabels(), rotation=0)

plt.suptitle('Promotional Effectiveness Analysis', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('outputs/visualizations/08_promotional_effectiveness.png', dpi=300, bbox_inches='tight')
plt.close()

# External Factors Impact
print("[6/7] External factors...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Temperature vs Sales
axes[0, 0].scatter(train['Temperature'], train['Weekly_Sales'], 
                   alpha=0.3, s=10, color='blue')
axes[0, 0].set_title('Temperature vs Sales', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Temperature (°F)', fontsize=11)
axes[0, 0].set_ylabel('Weekly Sales ($)', fontsize=11)
axes[0, 0].grid(True, alpha=0.3)

# Add trend line
z = np.polyfit(train['Temperature'].dropna(), train.loc[train['Temperature'].notna(), 'Weekly_Sales'], 1)
p = np.poly1d(z)
temp_sorted = sorted(train['Temperature'].dropna())
axes[0, 0].plot(temp_sorted, p(temp_sorted), "r--", linewidth=2, label='Trend')
axes[0, 0].legend()

# Fuel Price vs Sales
axes[0, 1].scatter(train['Fuel_Price'], train['Weekly_Sales'], 
                   alpha=0.3, s=10, color='green')
axes[0, 1].set_title('Fuel Price vs Sales', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Fuel Price ($/gallon)', fontsize=11)
axes[0, 1].set_ylabel('Weekly Sales ($)', fontsize=11)
axes[0, 1].grid(True, alpha=0.3)

# CPI vs Sales
axes[1, 0].scatter(train['CPI'], train['Weekly_Sales'], 
                   alpha=0.3, s=10, color='red')
axes[1, 0].set_title('CPI vs Sales', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Consumer Price Index', fontsize=11)
axes[1, 0].set_ylabel('Weekly Sales ($)', fontsize=11)
axes[1, 0].grid(True, alpha=0.3)

# Unemployment vs Sales
axes[1, 1].scatter(train['Unemployment'], train['Weekly_Sales'], 
                   alpha=0.3, s=10, color='orange')
axes[1, 1].set_title('Unemployment vs Sales', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Unemployment Rate (%)', fontsize=11)
axes[1, 1].set_ylabel('Weekly Sales ($)', fontsize=11)
axes[1, 1].grid(True, alpha=0.3)

plt.suptitle('External Factors Impact on Sales', fontsize=18, fontweight='bold', y=1.00)
plt.tight_layout()
plt.savefig('outputs/visualizations/09_external_factors_impact.png', dpi=300, bbox_inches='tight')
plt.close()

# Comprehensive Dashboard
print("[7/7] Comprehensive dashboard...")

fig = plt.figure(figsize=(20, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# 1. Sales over time
ax1 = fig.add_subplot(gs[0, :])
weekly_sales_plot = train.groupby('Date')['Weekly_Sales'].sum()
ax1.plot(weekly_sales_plot.index, weekly_sales_plot.values, color='blue', linewidth=1.5)
ax1.set_title('Total Weekly Sales Over Time', fontsize=14, fontweight='bold')
ax1.set_ylabel('Sales ($)', fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

# 2. Sales by store type (pie)
ax2 = fig.add_subplot(gs[1, 0])
type_totals = train.groupby('StoreType')['Weekly_Sales'].sum()
ax2.pie(type_totals.values, labels=type_totals.index, autopct='%1.1f%%', 
        colors=['#FF6B6B', '#4ECDC4', '#45B7D1'], startangle=90)
ax2.set_title('Sales Distribution by Store Type', fontsize=12, fontweight='bold')

# 3. Monthly average sales
ax3 = fig.add_subplot(gs[1, 1])
monthly_avg = train.groupby('Month')['Weekly_Sales'].mean()
ax3.bar(range(1, 13), monthly_avg.values, color='steelblue', edgecolor='black')
ax3.set_title('Average Sales by Month', fontsize=12, fontweight='bold')
ax3.set_xlabel('Month', fontsize=10)
ax3.set_ylabel('Avg Sales ($)', fontsize=10)
ax3.set_xticks(range(1, 13))
ax3.grid(axis='y', alpha=0.3)

# 4. Holiday vs non-holiday
ax4 = fig.add_subplot(gs[1, 2])
holiday_avg = train.groupby('IsHoliday')['Weekly_Sales'].mean()
ax4.bar(['Non-Holiday', 'Holiday'], holiday_avg.values, 
        color=['lightblue', 'coral'], edgecolor='black', linewidth=1.5)
ax4.set_title('Holiday vs Non-Holiday Sales', fontsize=12, fontweight='bold')
ax4.set_ylabel('Avg Sales ($)', fontsize=10)
ax4.grid(axis='y', alpha=0.3)

# 5. Top 10 departments
ax5 = fig.add_subplot(gs[2, 0])
top10_depts = train.groupby('Dept')['Weekly_Sales'].sum().nlargest(10)
ax5.barh(range(10), top10_depts.values[::-1], color='teal', edgecolor='black')
ax5.set_yticks(range(10))
ax5.set_yticklabels(top10_depts.index[::-1])
ax5.set_title('Top 10 Departments by Sales', fontsize=12, fontweight='bold')
ax5.set_xlabel('Total Sales ($)', fontsize=10)
ax5.grid(axis='x', alpha=0.3)
ax5.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.0f}M'))

# 6. Store size distribution
ax6 = fig.add_subplot(gs[2, 1])
store_sizes = train.groupby('Store')['Size'].first()
ax6.hist(store_sizes.values, bins=20, color='lightgreen', edgecolor='black', linewidth=1.2)
ax6.set_title('Store Size Distribution', fontsize=12, fontweight='bold')
ax6.set_xlabel('Store Size (sq ft)', fontsize=10)
ax6.set_ylabel('Count', fontsize=10)
ax6.grid(axis='y', alpha=0.3)

# 7. Sales volatility by quarter
ax7 = fig.add_subplot(gs[2, 2])
quarterly_std = train.groupby('Quarter')['Weekly_Sales'].std()
ax7.bar(range(1, 5), quarterly_std.values, color=['#FFB6C1', '#DDA0DD', '#98D8C8', '#FFD700'], 
        edgecolor='black', linewidth=1.5)
ax7.set_title('Sales Volatility by Quarter', fontsize=12, fontweight='bold')
ax7.set_xlabel('Quarter', fontsize=10)
ax7.set_ylabel('Std Dev ($)', fontsize=10)
ax7.set_xticks(range(1, 5))
ax7.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'])
ax7.grid(axis='y', alpha=0.3)

plt.suptitle('WALMART SALES FORECASTING - COMPREHENSIVE DASHBOARD', 
             fontsize=20, fontweight='bold', y=0.995)
plt.savefig('outputs/visualizations/10_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*80)
print("TASK 2.3 COMPLETE - Advanced Visualizations (7 plots created)")
print("="*80)

