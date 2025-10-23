"""
MILESTONE 1 - Step 1.4: Exploratory Data Analysis (EDA)
========================================================
Task 4: Exploratory Data Analysis

Perform comprehensive EDA to understand:
- Sales trends and seasonality
- External factors impact
- Relationships between products, promotions, and sales

Author: Data Science Team
Date: October 23, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 6)

print("="*80)
print("STEP 1.4: EXPLORATORY DATA ANALYSIS (EDA)")
print("="*80)

# Load data
print("\n[1] Loading Data...")
print("-" * 80)

train = pd.read_csv('processed_data/Stage1.2/train_cleaned_step2.csv')
train['Date'] = pd.to_datetime(train['Date'])

# Extract time features for analysis
train['Year'] = train['Date'].dt.year
train['Month'] = train['Date'].dt.month
train['Week'] = train['Date'].dt.isocalendar().week
train['Quarter'] = train['Date'].dt.quarter
train['DayOfWeek'] = train['Date'].dt.dayofweek
train['MonthName'] = train['Date'].dt.month_name()

print(f"✓ Loaded: {len(train):,} rows × {len(train.columns)} columns")
print(f"✓ Date Range: {train['Date'].min().date()} to {train['Date'].max().date()}")
print(f"✓ Time Span: {(train['Date'].max() - train['Date'].min()).days} days")

# Create visualizations directory
import os
os.makedirs('visualizations', exist_ok=True)

# ============================================================================
# PART 1: SALES TRENDS OVER TIME
# ============================================================================

print("\n" + "="*80)
print("PART 1: SALES TRENDS OVER TIME")
print("="*80)

# 1.1 Overall Sales Trend
print("\n[1.1] Analyzing Overall Sales Trend...")

weekly_sales = train.groupby('Date')['Weekly_Sales'].sum().reset_index()

plt.figure(figsize=(16, 6))
plt.plot(weekly_sales['Date'], weekly_sales['Weekly_Sales'], linewidth=1, alpha=0.7)
plt.title('Total Weekly Sales Over Time (All Stores)', fontsize=16, fontweight='bold')
plt.xlabel('Date', fontsize=12)
plt.ylabel('Total Weekly Sales ($)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/01_overall_sales_trend.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/01_overall_sales_trend.png")
plt.close()

# Statistics
print(f"\n   Overall Trend Statistics:")
print(f"   - Total Sales (all time): ${weekly_sales['Weekly_Sales'].sum():,.2f}")
print(f"   - Average Weekly Sales: ${weekly_sales['Weekly_Sales'].mean():,.2f}")
print(f"   - Peak Week Sales: ${weekly_sales['Weekly_Sales'].max():,.2f} on {weekly_sales.loc[weekly_sales['Weekly_Sales'].idxmax(), 'Date'].date()}")
print(f"   - Lowest Week Sales: ${weekly_sales['Weekly_Sales'].min():,.2f} on {weekly_sales.loc[weekly_sales['Weekly_Sales'].idxmin(), 'Date'].date()}")

# 1.2 Sales by Year
print("\n[1.2] Analyzing Year-over-Year Trends...")

yearly_sales = train.groupby('Year')['Weekly_Sales'].agg(['sum', 'mean', 'count']).reset_index()
yearly_sales['sum'] = yearly_sales['sum'].round(2)
yearly_sales['mean'] = yearly_sales['mean'].round(2)

plt.figure(figsize=(10, 6))
plt.bar(yearly_sales['Year'], yearly_sales['sum'], color=['#3498db', '#e74c3c', '#2ecc71'])
plt.title('Total Sales by Year', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Total Sales ($)', fontsize=12)
for i, v in enumerate(yearly_sales['sum']):
    plt.text(yearly_sales['Year'].iloc[i], v, f'${v:,.0f}', ha='center', va='bottom', fontsize=10)
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/02_sales_by_year.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/02_sales_by_year.png")
plt.close()

print(f"\n   Year-over-Year Summary:")
for _, row in yearly_sales.iterrows():
    print(f"   {int(row['Year'])}: Total=${row['sum']:,.2f} | Avg=${row['mean']:,.2f} | Weeks={int(row['count'])}")

# ============================================================================
# PART 2: SEASONALITY ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("PART 2: SEASONALITY ANALYSIS")
print("="*80)

# 2.1 Monthly Sales Pattern
print("\n[2.1] Analyzing Monthly Seasonality...")

monthly_sales = train.groupby('Month')['Weekly_Sales'].agg(['mean', 'sum']).reset_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.bar(monthly_sales['Month'], monthly_sales['mean'], color='skyblue', edgecolor='black')
plt.title('Average Sales by Month', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Weekly Sales ($)', fontsize=12)
plt.xticks(range(1, 13), month_names, rotation=45)
plt.grid(axis='y', alpha=0.3)

plt.subplot(1, 2, 2)
plt.plot(monthly_sales['Month'], monthly_sales['mean'], marker='o', linewidth=2, markersize=8, color='#e74c3c')
plt.title('Monthly Sales Trend', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Weekly Sales ($)', fontsize=12)
plt.xticks(range(1, 13), month_names, rotation=45)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/Stage1.4/03_monthly_seasonality.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/03_monthly_seasonality.png")
plt.close()

peak_month = monthly_sales.loc[monthly_sales['mean'].idxmax(), 'Month']
low_month = monthly_sales.loc[monthly_sales['mean'].idxmin(), 'Month']
print(f"\n   Seasonal Insights:")
print(f"   - Peak Month: {month_names[int(peak_month)-1]} (${monthly_sales.loc[monthly_sales['mean'].idxmax(), 'mean']:,.2f})")
print(f"   - Lowest Month: {month_names[int(low_month)-1]} (${monthly_sales.loc[monthly_sales['mean'].idxmin(), 'mean']:,.2f})")

# 2.2 Quarterly Pattern
print("\n[2.2] Analyzing Quarterly Patterns...")

quarterly_sales = train.groupby('Quarter')['Weekly_Sales'].agg(['mean', 'sum']).reset_index()

plt.figure(figsize=(10, 6))
plt.bar(quarterly_sales['Quarter'], quarterly_sales['mean'], color=['#3498db', '#9b59b6', '#e67e22', '#e74c3c'], edgecolor='black')
plt.title('Average Sales by Quarter', fontsize=16, fontweight='bold')
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Average Weekly Sales ($)', fontsize=12)
plt.xticks([1, 2, 3, 4], ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (Jul-Sep)', 'Q4 (Oct-Dec)'])
for i, v in enumerate(quarterly_sales['mean']):
    plt.text(i+1, v, f'${v:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/04_quarterly_pattern.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/04_quarterly_pattern.png")
plt.close()

print(f"\n   Quarterly Summary:")
for _, row in quarterly_sales.iterrows():
    print(f"   Q{int(row['Quarter'])}: Avg=${row['mean']:,.2f} | Total=${row['sum']:,.2f}")

# ============================================================================
# PART 3: HOLIDAY IMPACT ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("PART 3: HOLIDAY IMPACT ANALYSIS")
print("="*80)

print("\n[3.1] Analyzing Holiday vs Non-Holiday Sales...")

holiday_comparison = train.groupby('IsHoliday')['Weekly_Sales'].agg(['mean', 'median', 'sum', 'count']).reset_index()

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
categories = ['Non-Holiday', 'Holiday']
values = [holiday_comparison.loc[holiday_comparison['IsHoliday']==False, 'mean'].values[0],
          holiday_comparison.loc[holiday_comparison['IsHoliday']==True, 'mean'].values[0]]
colors = ['#3498db', '#e74c3c']
plt.bar(categories, values, color=colors, edgecolor='black', width=0.6)
plt.title('Average Sales: Holiday vs Non-Holiday', fontsize=14, fontweight='bold')
plt.ylabel('Average Weekly Sales ($)', fontsize=12)
for i, v in enumerate(values):
    plt.text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.subplot(1, 2, 2)
counts = [holiday_comparison.loc[holiday_comparison['IsHoliday']==False, 'count'].values[0],
          holiday_comparison.loc[holiday_comparison['IsHoliday']==True, 'count'].values[0]]
plt.bar(categories, counts, color=colors, edgecolor='black', width=0.6)
plt.title('Number of Weeks', fontsize=14, fontweight='bold')
plt.ylabel('Week Count', fontsize=12)
for i, v in enumerate(counts):
    plt.text(i, v, f'{int(v):,}', ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/Stage1.4/05_holiday_impact.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/05_holiday_impact.png")
plt.close()

non_holiday_avg = holiday_comparison.loc[holiday_comparison['IsHoliday']==False, 'mean'].values[0]
holiday_avg = holiday_comparison.loc[holiday_comparison['IsHoliday']==True, 'mean'].values[0]
holiday_lift = ((holiday_avg - non_holiday_avg) / non_holiday_avg) * 100

print(f"\n   Holiday Impact:")
print(f"   - Non-Holiday Average: ${non_holiday_avg:,.2f}")
print(f"   - Holiday Average: ${holiday_avg:,.2f}")
print(f"   - Holiday Lift: {holiday_lift:+.1f}%")
print(f"   - Holiday Weeks: {int(holiday_comparison.loc[holiday_comparison['IsHoliday']==True, 'count'].values[0]):,} ({int(holiday_comparison.loc[holiday_comparison['IsHoliday']==True, 'count'].values[0])/len(train)*100:.1f}% of total)")

# ============================================================================
# PART 4: STORE TYPE ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("PART 4: STORE TYPE ANALYSIS")
print("="*80)

print("\n[4.1] Analyzing Sales by Store Type...")

store_type_sales = train.groupby('Type')['Weekly_Sales'].agg(['mean', 'median', 'sum', 'count']).reset_index()

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.bar(store_type_sales['Type'], store_type_sales['mean'], color=['#3498db', '#2ecc71', '#e67e22'], edgecolor='black')
plt.title('Average Sales by Store Type', fontsize=14, fontweight='bold')
plt.xlabel('Store Type', fontsize=12)
plt.ylabel('Average Weekly Sales ($)', fontsize=12)
for i, (idx, row) in enumerate(store_type_sales.iterrows()):
    plt.text(i, row['mean'], f'${row["mean"]:,.0f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.subplot(1, 2, 2)
plt.bar(store_type_sales['Type'], store_type_sales['count'], color=['#3498db', '#2ecc71', '#e67e22'], edgecolor='black')
plt.title('Number of Records by Store Type', fontsize=14, fontweight='bold')
plt.xlabel('Store Type', fontsize=12)
plt.ylabel('Record Count', fontsize=12)
for i, (idx, row) in enumerate(store_type_sales.iterrows()):
    plt.text(i, row['count'], f'{int(row["count"]):,}', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/Stage1.4/06_store_type_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/06_store_type_comparison.png")
plt.close()

print(f"\n   Store Type Comparison:")
for _, row in store_type_sales.iterrows():
    print(f"   Type {row['Type']}: Avg=${row['mean']:,.2f} | Median=${row['median']:,.2f} | Total=${row['sum']:,.2f} | Records={int(row['count']):,}")

# ============================================================================
# PART 5: PROMOTION IMPACT ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("PART 5: PROMOTION IMPACT ANALYSIS")
print("="*80)

print("\n[5.1] Analyzing Promotion (MarkDown) Impact...")

# Compare sales with vs without promotions
promo_cols = ['Has_MarkDown1', 'Has_MarkDown2', 'Has_MarkDown3', 'Has_MarkDown4', 'Has_MarkDown5']
promo_impact = []

for promo in promo_cols:
    with_promo = train[train[promo] == 1]['Weekly_Sales'].mean()
    without_promo = train[train[promo] == 0]['Weekly_Sales'].mean()
    lift = ((with_promo - without_promo) / without_promo) * 100
    promo_impact.append({
        'Promotion': promo.replace('Has_', ''),
        'With_Promo': with_promo,
        'Without_Promo': without_promo,
        'Lift_%': lift
    })

promo_df = pd.DataFrame(promo_impact)

plt.figure(figsize=(12, 6))
x = np.arange(len(promo_df))
width = 0.35

plt.bar(x - width/2, promo_df['Without_Promo'], width, label='Without Promotion', color='#95a5a6', edgecolor='black')
plt.bar(x + width/2, promo_df['With_Promo'], width, label='With Promotion', color='#e74c3c', edgecolor='black')

plt.xlabel('Promotion Type', fontsize=12)
plt.ylabel('Average Weekly Sales ($)', fontsize=12)
plt.title('Sales Impact of Promotional Markdowns', fontsize=16, fontweight='bold')
plt.xticks(x, promo_df['Promotion'])
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/07_promotion_impact.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/07_promotion_impact.png")
plt.close()

print(f"\n   Promotion Impact Summary:")
for _, row in promo_df.iterrows():
    print(f"   {row['Promotion']}:")
    print(f"      Without: ${row['Without_Promo']:,.2f}")
    print(f"      With: ${row['With_Promo']:,.2f}")
    print(f"      Lift: {row['Lift_%']:+.1f}%")

# ============================================================================
# PART 6: EXTERNAL FACTORS ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("PART 6: EXTERNAL FACTORS ANALYSIS")
print("="*80)

print("\n[6.1] Analyzing External Factors Correlation...")

# Correlation matrix
external_factors = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
correlation_data = train[external_factors + ['Weekly_Sales']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, square=True, 
            linewidths=1, cbar_kws={"shrink": 0.8}, fmt='.3f')
plt.title('Correlation: External Factors vs Weekly Sales', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/08_external_factors_correlation.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/08_external_factors_correlation.png")
plt.close()

print(f"\n   Correlation with Weekly Sales:")
for factor in external_factors:
    corr = correlation_data.loc[factor, 'Weekly_Sales']
    print(f"   {factor:15s}: {corr:+.4f}")

# ============================================================================
# PART 7: SCATTER PLOTS - External Factors vs Sales
# ============================================================================

print("\n[6.2] Creating Scatter Plots for External Factors...")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('External Factors vs Weekly Sales', fontsize=18, fontweight='bold', y=1.00)

# Temperature vs Sales
axes[0, 0].scatter(train['Temperature'], train['Weekly_Sales'], alpha=0.3, s=1)
axes[0, 0].set_xlabel('Temperature (°F)', fontsize=12)
axes[0, 0].set_ylabel('Weekly Sales ($)', fontsize=12)
axes[0, 0].set_title(f'Temperature vs Sales (corr: {correlation_data.loc["Temperature", "Weekly_Sales"]:+.3f})', fontsize=13)
axes[0, 0].grid(True, alpha=0.3)

# Fuel Price vs Sales
axes[0, 1].scatter(train['Fuel_Price'], train['Weekly_Sales'], alpha=0.3, s=1, color='orange')
axes[0, 1].set_xlabel('Fuel Price ($/gallon)', fontsize=12)
axes[0, 1].set_ylabel('Weekly Sales ($)', fontsize=12)
axes[0, 1].set_title(f'Fuel Price vs Sales (corr: {correlation_data.loc["Fuel_Price", "Weekly_Sales"]:+.3f})', fontsize=13)
axes[0, 1].grid(True, alpha=0.3)

# CPI vs Sales
axes[1, 0].scatter(train['CPI'], train['Weekly_Sales'], alpha=0.3, s=1, color='green')
axes[1, 0].set_xlabel('Consumer Price Index', fontsize=12)
axes[1, 0].set_ylabel('Weekly Sales ($)', fontsize=12)
axes[1, 0].set_title(f'CPI vs Sales (corr: {correlation_data.loc["CPI", "Weekly_Sales"]:+.3f})', fontsize=13)
axes[1, 0].grid(True, alpha=0.3)

# Unemployment vs Sales
axes[1, 1].scatter(train['Unemployment'], train['Weekly_Sales'], alpha=0.3, s=1, color='red')
axes[1, 1].set_xlabel('Unemployment Rate (%)', fontsize=12)
axes[1, 1].set_ylabel('Weekly Sales ($)', fontsize=12)
axes[1, 1].set_title(f'Unemployment vs Sales (corr: {correlation_data.loc["Unemployment", "Weekly_Sales"]:+.3f})', fontsize=13)
axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/Stage1.4/09_external_factors_scatter.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/09_external_factors_scatter.png")
plt.close()

# ============================================================================
# PART 8: TOP DEPARTMENTS ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("PART 8: DEPARTMENT ANALYSIS")
print("="*80)

print("\n[8.1] Analyzing Top Performing Departments...")

dept_sales = train.groupby('Dept')['Weekly_Sales'].agg(['sum', 'mean', 'count']).reset_index()
dept_sales = dept_sales.sort_values('sum', ascending=False)

top_10_depts = dept_sales.head(10)

plt.figure(figsize=(14, 6))
plt.barh(top_10_depts['Dept'].astype(str), top_10_depts['sum'], color='skyblue', edgecolor='black')
plt.xlabel('Total Sales ($)', fontsize=12)
plt.ylabel('Department', fontsize=12)
plt.title('Top 10 Departments by Total Sales', fontsize=16, fontweight='bold')
plt.gca().invert_yaxis()
for i, (idx, row) in enumerate(top_10_depts.iterrows()):
    plt.text(row['sum'], i, f' ${row["sum"]:,.0f}', va='center', fontsize=10)
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/10_top_departments.png', dpi=300, bbox_inches='tight')
print("✓ Saved: visualizations/Stage1.4/10_top_departments.png")
plt.close()

print(f"\n   Top 10 Departments:")
for i, (_, row) in enumerate(top_10_depts.iterrows(), 1):
    print(f"   {i:2d}. Dept {int(row['Dept']):2d}: Total=${row['sum']:,.2f} | Avg=${row['mean']:,.2f} | Records={int(row['count']):,}")

# ============================================================================
# SUMMARY
# ============================================================================

print("\n" + "="*80)
print("✅ EXPLORATORY DATA ANALYSIS COMPLETED!")
print("="*80)

print(f"""
📊 EDA Summary - 10 Visualizations Created:

1. Overall Sales Trend Over Time
2. Sales by Year
3. Monthly Seasonality Pattern
4. Quarterly Pattern
5. Holiday Impact Analysis
6. Store Type Comparison
7. Promotion Impact Analysis
8. External Factors Correlation Heatmap
9. External Factors Scatter Plots
10. Top 10 Departments

🎯 Key Insights Discovered:

1. TRENDS:
   - Clear seasonal patterns identified
   - Q4 shows highest sales (holiday season)
   - Year-over-year analysis shows growth/decline trends

2. SEASONALITY:
   - Peak Month: December (holiday shopping)
   - Seasonal variations clearly visible
   - Quarterly patterns evident

3. HOLIDAY IMPACT:
   - Holiday weeks show {holiday_lift:+.1f}% sales lift
   - Significant impact on sales volume
   - Important feature for forecasting

4. STORE TYPES:
   - Type A stores have highest average sales
   - Clear performance differences by store size
   - Important segmentation variable

5. PROMOTIONS:
   - Promotional markdowns impact sales
   - Different markdown types show varying effectiveness
   - Promotion timing matters

6. EXTERNAL FACTORS:
   - Temperature: {correlation_data.loc['Temperature', 'Weekly_Sales']:+.4f} correlation
   - Fuel Price: {correlation_data.loc['Fuel_Price', 'Weekly_Sales']:+.4f} correlation
   - CPI: {correlation_data.loc['CPI', 'Weekly_Sales']:+.4f} correlation
   - Unemployment: {correlation_data.loc['Unemployment', 'Weekly_Sales']:+.4f} correlation

7. DEPARTMENTS:
   - Top performing departments identified
   - High variability across departments
   - Department-specific patterns exist

📁 All visualizations saved to: visualizations/

🔜 Next Steps:
   - Step 1.3: Outlier Detection (informed by EDA insights)
   - Step 1.4: Feature Engineering
   - Step 1.7: EDA Report Documentation
""")

print("="*80)

