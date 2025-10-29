"""
MILESTONE 1 - Step 1.4: Exploratory Data Analysis (EDA)
========================================================
Task 4: Exploratory Data Analysis

Perform comprehensive EDA to understand:
- Sales trends and seasonality
- External factors impact
- Relationships between products, promotions, and sales

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (14, 6)

print("="*80)
print("STEP 1.4: EXPLORATORY DATA ANALYSIS (EDA)")
print("="*80)

print("\n[1] Loading data...")
train = pd.read_csv('processed_data/Stage1.2/train_cleaned_step2.csv')
train['Date'] = pd.to_datetime(train['Date'])
train['Year'] = train['Date'].dt.year
train['Month'] = train['Date'].dt.month
train['Quarter'] = train['Date'].dt.quarter
print(f"✓ Loaded: {train.shape}")

os.makedirs('visualizations/Stage1.4', exist_ok=True)

print("\n[2] Analyzing sales trends...")

# Overall sales trend
weekly_sales = train.groupby('Date')['Weekly_Sales'].sum().reset_index()
plt.figure(figsize=(16, 6))
plt.plot(weekly_sales['Date'], weekly_sales['Weekly_Sales'], linewidth=1, alpha=0.7)
plt.title('Total Weekly Sales Over Time (All Stores)', fontsize=16, fontweight='bold')
plt.xlabel('Date')
plt.ylabel('Total Weekly Sales ($)')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/01_overall_sales_trend.png', dpi=300, bbox_inches='tight')
plt.close()

# Sales by year
yearly_sales = train.groupby('Year')['Weekly_Sales'].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.bar(yearly_sales['Year'], yearly_sales['sum'], color=['#3498db', '#e74c3c', '#2ecc71'])
plt.title('Total Sales by Year', fontsize=16, fontweight='bold')
plt.xlabel('Year')
plt.ylabel('Total Sales ($)')
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/02_sales_by_year.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n[3] Analyzing seasonality...")

# Monthly sales
monthly_sales = train.groupby('Month')['Weekly_Sales'].mean().reset_index()
month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.bar(monthly_sales['Month'], monthly_sales['Weekly_Sales'], color='skyblue', edgecolor='black')
plt.title('Average Sales by Month')
plt.xlabel('Month')
plt.ylabel('Average Weekly Sales ($)')
plt.xticks(range(1, 13), month_names, rotation=45)
plt.subplot(1, 2, 2)
plt.plot(monthly_sales['Month'], monthly_sales['Weekly_Sales'], marker='o', linewidth=2, color='#e74c3c')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Average Weekly Sales ($)')
plt.xticks(range(1, 13), month_names, rotation=45)
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/03_monthly_seasonality.png', dpi=300, bbox_inches='tight')
plt.close()

# Quarterly pattern
quarterly_sales = train.groupby('Quarter')['Weekly_Sales'].mean().reset_index()
plt.figure(figsize=(10, 6))
plt.bar(quarterly_sales['Quarter'], quarterly_sales['Weekly_Sales'], 
        color=['#3498db', '#9b59b6', '#e67e22', '#e74c3c'], edgecolor='black')
plt.title('Average Sales by Quarter', fontsize=16, fontweight='bold')
plt.xlabel('Quarter')
plt.ylabel('Average Weekly Sales ($)')
plt.xticks([1, 2, 3, 4], ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (Jul-Sep)', 'Q4 (Oct-Dec)'])
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/04_quarterly_pattern.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n[4] Analyzing holiday impact...")

# Holiday comparison
holiday_comparison = train.groupby('IsHoliday')['Weekly_Sales'].agg(['mean', 'count']).reset_index()
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
categories = ['Non-Holiday', 'Holiday']
values = [holiday_comparison.loc[0, 'mean'], holiday_comparison.loc[1, 'mean']]
plt.bar(categories, values, color=['#3498db', '#e74c3c'], edgecolor='black')
plt.title('Average Sales: Holiday vs Non-Holiday')
plt.ylabel('Average Weekly Sales ($)')
plt.subplot(1, 2, 2)
counts = [holiday_comparison.loc[0, 'count'], holiday_comparison.loc[1, 'count']]
plt.bar(categories, counts, color=['#3498db', '#e74c3c'], edgecolor='black')
plt.title('Number of Weeks')
plt.ylabel('Week Count')
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/05_holiday_impact.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n[5] Analyzing store types...")

# Store type comparison
store_type_sales = train.groupby('Type')['Weekly_Sales'].agg(['mean', 'count']).reset_index()
plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.bar(store_type_sales['Type'], store_type_sales['mean'], 
        color=['#3498db', '#2ecc71', '#e67e22'], edgecolor='black')
plt.title('Average Sales by Store Type')
plt.xlabel('Store Type')
plt.ylabel('Average Weekly Sales ($)')
plt.subplot(1, 2, 2)
plt.bar(store_type_sales['Type'], store_type_sales['count'], 
        color=['#3498db', '#2ecc71', '#e67e22'], edgecolor='black')
plt.title('Number of Records by Store Type')
plt.xlabel('Store Type')
plt.ylabel('Record Count')
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/06_store_type_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n[6] Analyzing promotion impact...")

# Promotion impact
promo_cols = ['Has_MarkDown1', 'Has_MarkDown2', 'Has_MarkDown3', 'Has_MarkDown4', 'Has_MarkDown5']
promo_impact = []
for promo in promo_cols:
    with_promo = train[train[promo] == 1]['Weekly_Sales'].mean()
    without_promo = train[train[promo] == 0]['Weekly_Sales'].mean()
    promo_impact.append({
        'Promotion': promo.replace('Has_', ''),
        'With_Promo': with_promo,
        'Without_Promo': without_promo
    })
promo_df = pd.DataFrame(promo_impact)

plt.figure(figsize=(12, 6))
x = np.arange(len(promo_df))
width = 0.35
plt.bar(x - width/2, promo_df['Without_Promo'], width, label='Without Promotion', 
        color='#95a5a6', edgecolor='black')
plt.bar(x + width/2, promo_df['With_Promo'], width, label='With Promotion', 
        color='#e74c3c', edgecolor='black')
plt.xlabel('Promotion Type')
plt.ylabel('Average Weekly Sales ($)')
plt.title('Sales Impact of Promotional Markdowns')
plt.xticks(x, promo_df['Promotion'])
plt.legend()
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/07_promotion_impact.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n[7] Analyzing external factors...")

# Correlation heatmap
external_factors = ['Temperature', 'Fuel_Price', 'CPI', 'Unemployment']
correlation_data = train[external_factors + ['Weekly_Sales']].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', center=0, square=True, 
            linewidths=1, cbar_kws={"shrink": 0.8}, fmt='.3f')
plt.title('Correlation: External Factors vs Weekly Sales')
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/08_external_factors_correlation.png', dpi=300, bbox_inches='tight')
plt.close()

# Scatter plots
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes[0, 0].scatter(train['Temperature'], train['Weekly_Sales'], alpha=0.3, s=1)
axes[0, 0].set_xlabel('Temperature (°F)')
axes[0, 0].set_ylabel('Weekly Sales ($)')
axes[0, 0].set_title('Temperature vs Sales')

axes[0, 1].scatter(train['Fuel_Price'], train['Weekly_Sales'], alpha=0.3, s=1, color='orange')
axes[0, 1].set_xlabel('Fuel Price ($/gallon)')
axes[0, 1].set_ylabel('Weekly Sales ($)')
axes[0, 1].set_title('Fuel Price vs Sales')

axes[1, 0].scatter(train['CPI'], train['Weekly_Sales'], alpha=0.3, s=1, color='green')
axes[1, 0].set_xlabel('Consumer Price Index')
axes[1, 0].set_ylabel('Weekly Sales ($)')
axes[1, 0].set_title('CPI vs Sales')

axes[1, 1].scatter(train['Unemployment'], train['Weekly_Sales'], alpha=0.3, s=1, color='red')
axes[1, 1].set_xlabel('Unemployment Rate (%)')
axes[1, 1].set_ylabel('Weekly Sales ($)')
axes[1, 1].set_title('Unemployment vs Sales')

plt.tight_layout()
plt.savefig('visualizations/Stage1.4/09_external_factors_scatter.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n[8] Analyzing departments...")

# Top departments
dept_sales = train.groupby('Dept')['Weekly_Sales'].sum().reset_index().sort_values('Weekly_Sales', ascending=False).head(10)
plt.figure(figsize=(14, 6))
plt.barh(dept_sales['Dept'].astype(str), dept_sales['Weekly_Sales'], color='skyblue', edgecolor='black')
plt.xlabel('Total Sales ($)')
plt.ylabel('Department')
plt.title('Top 10 Departments by Total Sales')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('visualizations/Stage1.4/10_top_departments.png', dpi=300, bbox_inches='tight')
plt.close()

print("✓ Created 10 visualization files")

print("\n" + "="*80)
print("EXPLORATORY DATA ANALYSIS COMPLETED!")
print("="*80)
