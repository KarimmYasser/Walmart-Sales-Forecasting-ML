"""
MILESTONE 1 - Step 1.3: Outlier Detection & Analysis
=====================================================
Task 2: Data Exploration (Continued)

Detect and analyze outliers in sales data to understand their nature
and decide on appropriate treatment strategy.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os


sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*80)
print("STEP 1.3: OUTLIER DETECTION & ANALYSIS")
print("="*80)

print("\n[1] Loading cleaned data...")
train = pd.read_csv('processed_data/Stage1.2/train_cleaned_step2.csv')
train['Date'] = pd.to_datetime(train['Date'])
print(f"Loaded: {train.shape}")

print("\n[2] Analyzing outliers using IQR method...")
Q1 = train['Weekly_Sales'].quantile(0.25)
Q3 = train['Weekly_Sales'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers_lower = train[train['Weekly_Sales'] < lower_bound]
outliers_upper = train[train['Weekly_Sales'] > upper_bound]
total_outliers = len(outliers_lower) + len(outliers_upper)
print(f"Found {total_outliers:,} outliers ({total_outliers/len(train)*100:.2f}%)")

print("\n[3] Creating visualizations...")
os.makedirs('visualizations/Stage1.3', exist_ok=True)

# Box plot by store type
plt.figure(figsize=(10, 6))
train.boxplot(column='Weekly_Sales', by='Type', figsize=(10, 6))
plt.title('Weekly Sales Distribution by Store Type')
plt.suptitle('')
plt.xlabel('Store Type')
plt.ylabel('Weekly Sales ($)')
plt.tight_layout()
plt.savefig('visualizations/Stage1.3/boxplot_sales_by_type.png', dpi=300, bbox_inches='tight')
plt.close()

# Histogram
plt.figure(figsize=(12, 6))
plt.hist(train['Weekly_Sales'], bins=100, edgecolor='black', alpha=0.7)
plt.axvline(lower_bound, color='r', linestyle='--', label=f'Lower Bound: ${lower_bound:,.0f}')
plt.axvline(upper_bound, color='r', linestyle='--', label=f'Upper Bound: ${upper_bound:,.0f}')
plt.xlabel('Weekly Sales ($)')
plt.ylabel('Frequency')
plt.title('Distribution of Weekly Sales with IQR Bounds')
plt.legend()
plt.tight_layout()
plt.savefig('visualizations/Stage1.3/histogram_sales_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Holiday impact boxplot
plt.figure(figsize=(10, 6))
train.boxplot(column='Weekly_Sales', by='IsHoliday', figsize=(10, 6))
plt.title('Weekly Sales: Holiday vs Non-Holiday')
plt.suptitle('')
plt.xlabel('Is Holiday Week?')
plt.ylabel('Weekly Sales ($)')
plt.xticks([1, 2], ['Non-Holiday', 'Holiday'])
plt.tight_layout()
plt.savefig('visualizations/Stage1.3/boxplot_holiday_impact.png', dpi=300, bbox_inches='tight')
plt.close()

# Sales over time
plt.figure(figsize=(14, 6))
plt.scatter(train['Date'], train['Weekly_Sales'], alpha=0.3, s=1)
plt.axhline(upper_bound, color='r', linestyle='--', alpha=0.7, label=f'Upper Bound: ${upper_bound:,.0f}')
plt.axhline(lower_bound, color='r', linestyle='--', alpha=0.7, label=f'Lower Bound: ${lower_bound:,.0f}')
plt.xlabel('Date')
plt.ylabel('Weekly Sales ($)')
plt.title('Weekly Sales Over Time with Outlier Bounds')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('visualizations/Stage1.3/scatter_sales_over_time.png', dpi=300, bbox_inches='tight')
plt.close()

print("Saved 4 visualization files")

print("\n[4] Decision: Keep all outliers (valid business scenarios)")

print("\n" + "="*80)
print("STEP 1.3 COMPLETED!")
print("="*80)
