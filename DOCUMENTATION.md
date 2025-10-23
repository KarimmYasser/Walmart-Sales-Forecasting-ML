# Walmart Sales Forecasting Project - Documentation

**Project Name:** Walmart Weekly Sales Forecasting  
**Dataset:** Walmart Recruiting Store Sales Forecasting  
**Start Date:** October 23, 2025  
**Team:** Data Science Team  

---

## 📑 Table of Contents

1. [Project Overview](#project-overview)
2. [Dataset Description](#dataset-description)
3. [Milestone 1: Data Collection & Preprocessing](#milestone-1-data-collection--preprocessing)
   - [Step 1.1: Data Loading & Merging](#step-11-data-loading--merging)
   - [Step 1.2: Handling Missing Values](#step-12-handling-missing-values)
   - [Step 1.3: Outlier Detection](#step-13-outlier-detection)
   - [Step 1.4: Feature Engineering](#step-14-feature-engineering)
   - [Step 1.5: Encoding Categorical Features](#step-15-encoding-categorical-features)

---

## 📊 Project Overview

### Business Problem
Walmart needs to forecast weekly sales across 45 stores and 99 departments to optimize:
- **Inventory Management**: Prevent stockouts and overstocking
- **Staff Scheduling**: Allocate resources based on predicted demand
- **Marketing Planning**: Plan promotions during high-sales periods
- **Financial Planning**: Accurate revenue projections

### Objective
Build a machine learning model to predict weekly sales for each store-department combination, considering:
- Historical sales patterns
- Store characteristics (type, size)
- External factors (temperature, fuel price, CPI, unemployment)
- Holiday effects
- Promotional markdowns

### Success Metrics
- **MAE (Mean Absolute Error)**: < $3,000 per week
- **RMSE (Root Mean Square Error)**: < $5,000 per week
- **MAPE (Mean Absolute Percentage Error)**: < 15%
- Beat baseline model (naive forecasting) by at least 25%

---

## 📦 Dataset Description

### Source Files

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| `train.csv` | 421,570 | 5 | Historical weekly sales (2010-02-05 to 2012-10-26) |
| `test.csv` | 115,064 | 4 | Test period data (2012-11-02 to 2013-07-26) |
| `stores.csv` | 45 | 3 | Store metadata (type, size) |
| `features.xlsx` | 8,190 | 12 | External features (temperature, markdowns, etc.) |

### Processed Files 

**After Step 1.1 (Merging):**
| File | Rows | Columns | Size | Description |
|------|------|---------|------|-------------|
| `train_merged.csv` | 421,570 | 16 | 34.08 MB | Training data with all features + Weekly_Sales |
| `test_merged.csv` | 115,064 | 15 | 9.87 MB | Test data with all features (NO Weekly_Sales) |

**After Step 1.2 (Missing Values Handled):**
| File | Rows | Columns | Size | Description |
|------|------|---------|------|-------------|
| `train_cleaned_step2.csv` | 421,570 | 21 | ~38 MB | Clean training data, 100% complete |
| `test_cleaned_step2.csv` | 115,064 | 20 | ~11 MB | Clean test data, 100% complete |

### Dataset Schema

#### Train Data (`train.csv`)
- `Store` (int): Store number (1-45)
- `Dept` (int): Department number (1-99)
- `Date` (date): Week ending date
- `Weekly_Sales` (float): Sales for the store-department (TARGET VARIABLE)
- `IsHoliday` (bool): Whether the week contains a major holiday

#### Stores Data (`stores.csv`)
- `Store` (int): Store number
- `Type` (categorical): Store type [A, B, C]
  - Type A: 22 stores (large supercenters)
  - Type B: 17 stores (medium-sized)
  - Type C: 6 stores (small stores)
- `Size` (int): Store size in square feet

#### Features Data (`features.xlsx`)
- `Store`, `Date`, `IsHoliday`: Matching keys
- `Temperature` (float): Average temperature in the region (°F)
- `Fuel_Price` (float): Cost of fuel in the region ($/gallon)
- `MarkDown1-5` (float): Anonymized promotional markdowns (high missing %)
- `CPI` (float): Consumer Price Index
- `Unemployment` (float): Unemployment rate (%)

### Key Observations
- **Time Span**: ~3.5 years of data (2010-2013)
- **Granularity**: Weekly level
- **Target Variable**: Weekly_Sales (can be negative due to returns)
- **Missing Data**: Significant in MarkDown columns (50-64% missing)
- **Holidays**: Super Bowl, Labor Day, Thanksgiving, Christmas

---

## 🎯 Understanding Train vs Test Data

### Critical Difference

**THE KEY POINT:** Both datasets contain **REAL historical Walmart data**. Nothing is predicted yet!

| Aspect | train_merged.csv | test_merged.csv |
|--------|------------------|-----------------|
| **Has Weekly_Sales?** | ✅ YES (Target variable) | ❌ NO (We must predict this!) |
| **Rows** | 421,570 | 115,064 |
| **Columns** | 16 | 15 |
| **Date Range** | 2010-02-05 to 2012-10-26 | 2012-11-02 to 2013-07-26 |
| **Purpose** | LEARN patterns from past | PREDICT future sales |
| **Usage** | Training & validation | Making predictions |

### Why is Weekly_Sales Missing in Test?

Walmart **intentionally removed** the `Weekly_Sales` column to simulate a real forecasting scenario:
- The sales **did happen** in real life (Nov 2012 - Jul 2013)
- Walmart **knows** what they were
- They **hide** them from us to create a challenge
- We **predict** them using our model
- We can **evaluate** accuracy by comparing predictions to actuals

### Timeline Visualization

```
┌─────────────────────────────────────────────────────────────┐
│  2010          2011          2012          2013             │
├─────────────────────────────────────────────────────────────┤
│  │◄────────── TRAIN DATA ──────────►│ 7d │◄─── TEST ────►│ │
│  Feb'10                         Oct'12 gap Nov'12    Jul'13│
│                                          │                   │
│  Learn from past (WITH sales data)      │  Predict future  │
└─────────────────────────────────────────────────────────────┘
```

### Which Data to Use When?

**Current Phase (Milestones 1-3):**
- **Use:** `train_merged.csv` exclusively
- **Why:** Need the target variable to learn patterns and train models
- **Steps:** All preprocessing, EDA, feature engineering, model training

**Later Phase (Milestone 3 - Final Predictions):**
- **Use:** `test_merged.csv`
- **Why:** Make predictions on "future" data
- **Steps:** Apply same preprocessing, load trained model, predict sales

**Workflow Summary:**
```
train_merged.csv → Clean → Analyze → Train Model → Save model.pkl
                                           ↓
test_merged.csv → Same Preprocessing → Load Model → Predict → predictions.csv
```

---

## 🎯 Milestone 1: Data Collection & Preprocessing

### Overview
This milestone focuses on preparing the raw data for analysis and modeling. Data quality directly impacts model performance, so we invest significant effort here.

---

### Step 1.1: Data Loading & Merging

**📅 Completed:** October 23, 2025  
**⏱ Time Spent:** 1 hour  
**📄 Script:** `step_1_1_data_loading_merging.py`

#### Objective
Load all four datasets and merge them into a unified dataset for analysis and modeling.

#### Implementation Details

##### 1. Data Loading
Loaded each dataset with initial validation:

```python
import pandas as pd

# Load all datasets
train = pd.read_csv('datasets/walmart-recruiting-store-sales-forecasting/train.csv')
test = pd.read_csv('datasets/walmart-recruiting-store-sales-forecasting/test.csv')
stores = pd.read_csv('datasets/walmart-recruiting-store-sales-forecasting/stores.csv')
features = pd.read_excel('datasets/walmart-recruiting-store-sales-forecasting/features.xlsx')
```

**Initial Dataset Sizes:**
- Train: 421,570 rows × 5 columns
- Test: 115,064 rows × 4 columns
- Stores: 45 rows × 3 columns
- Features: 8,190 rows × 12 columns

##### 2. Data Quality Checks
Before merging, performed validation checks:

✅ **Duplicate Check:**
- Train: 0 duplicates on (Store, Dept, Date)
- Features: 0 duplicates on (Store, Date)

✅ **Missing Values Check:**
- Train: No missing values ✓
- Test: No missing values ✓
- Stores: No missing values ✓
- Features: Significant missing in MarkDown columns (addressed in Step 1.2)

⚠️ **Sales Data Anomalies:**
- Found negative sales values (returns/clearances)
- Min Sales: $-4,988.94
- Max Sales: $693,099.36
- These are valid business cases and will be kept

##### 3. Merging Strategy

**Merge 1: Train + Stores**
```python
train_full = train.merge(stores, on='Store', how='left')
```
- Merge Type: LEFT JOIN (keep all train records)
- Key: `Store`
- Result: Added `Type` and `Size` columns
- Validation: ✓ No null values after merge (all stores matched)

**Merge 2: Train+Stores + Features**
```python
# Convert dates to datetime
train_full['Date'] = pd.to_datetime(train_full['Date'])
features['Date'] = pd.to_datetime(features['Date'])

# Merge on Store, Date, and IsHoliday
train_full = train_full.merge(features, 
                               on=['Store', 'Date', 'IsHoliday'], 
                               how='left')
```
- Merge Type: LEFT JOIN
- Keys: `Store`, `Date`, `IsHoliday`
- Result: Added 9 feature columns (Temperature, Fuel_Price, MarkDown1-5, CPI, Unemployment)
- Some feature records not matched (will show as NaN)

**Merge 3: Test Dataset Preparation**
```python
test_full = test.merge(stores, on='Store', how='left')
test_full = test_full.merge(features, on=['Store', 'Date', 'IsHoliday'], how='left')
```
- Same structure as training data (minus Weekly_Sales)
- Ensures consistency for final predictions

##### 4. Final Dataset Structure

**Training Dataset (train_full):**
- **Shape:** 421,570 rows × 17 columns
- **Date Range:** 2010-02-05 to 2012-10-26
- **Columns:**

| # | Column Name | Data Type | Null Count | Null % | Description |
|---|------------|-----------|------------|--------|-------------|
| 1 | Store | int64 | 0 | 0.0% | Store ID (1-45) |
| 2 | Dept | int64 | 0 | 0.0% | Department ID (1-99) |
| 3 | Date | datetime64 | 0 | 0.0% | Week ending date |
| 4 | Weekly_Sales | float64 | 0 | 0.0% | **Target Variable** |
| 5 | IsHoliday | bool | 0 | 0.0% | Holiday indicator |
| 6 | Type | object | 0 | 0.0% | Store type (A/B/C) |
| 7 | Size | int64 | 0 | 0.0% | Store size (sq ft) |
| 8 | Temperature | float64 | varies | - | Average temperature |
| 9 | Fuel_Price | float64 | varies | - | Fuel cost |
| 10 | MarkDown1 | float64 | ~50% | - | Promotional markdown |
| 11 | MarkDown2 | float64 | ~64% | - | Promotional markdown |
| 12 | MarkDown3 | float64 | ~55% | - | Promotional markdown |
| 13 | MarkDown4 | float64 | ~57% | - | Promotional markdown |
| 14 | MarkDown5 | float64 | ~50% | - | Promotional markdown |
| 15 | CPI | float64 | varies | - | Consumer Price Index |
| 16 | Unemployment | float64 | varies | - | Unemployment rate |

**Test Dataset (test_full):**
- **Shape:** 115,064 rows × 16 columns (no Weekly_Sales)
- **Date Range:** 2012-11-02 to 2013-07-26

##### 5. Data Persistence

Created output directory and saved processed data:

```
processed_data/
├── train_merged.csv    (~85 MB)
└── test_merged.csv     (~25 MB)
```

These files will be used as input for subsequent preprocessing steps.

#### Results Summary

✅ **Achievements:**
1. Successfully loaded all 4 datasets
2. Performed data quality validation
3. Merged datasets with proper join logic
4. Created unified training and test datasets
5. Saved processed data for next steps

📊 **Statistics:**
- Training Records: 421,570
- Test Records: 115,064
- Features per Record: 17 (train), 16 (test)
- Data Coverage: 3.5 years

⚠️ **Issues Identified:**
1. Significant missing values in MarkDown columns → **Address in Step 1.2**
2. Some missing CPI/Unemployment values → **Address in Step 1.2**
3. Negative sales values exist → **Analyze in Step 1.3**

#### Sample Output

**First 5 rows of merged dataset:**
```
   Store  Dept       Date  Weekly_Sales  IsHoliday Type    Size  Temperature  ...
0      1     1 2010-02-05      24924.50      False    A  151315        42.31  ...
1      1     1 2010-02-12      46039.49       True    A  151315        38.51  ...
2      1     1 2010-02-19      41595.55      False    A  151315        39.93  ...
3      1     1 2010-02-26      19403.54      False    A  151315        46.63  ...
4      1     1 2010-03-05      21827.90      False    A  151315        46.50  ...
```

**Store-Department Time Series Example (Store 1, Dept 1):**
- Shows weekly variation in sales
- Holiday weeks show spikes (e.g., row 1 → row 2: +85% increase)
- Temperature and other features vary by week

#### Next Steps

🔜 **Step 1.2:** Handling Missing Values
- Strategy for MarkDown columns (50-64% missing)
- Imputation for CPI/Unemployment
- Decision on keeping vs. dropping features

---

### Step 1.2: Handling Missing Values (Train & Test)

**📅 Completed:** October 23, 2025  
**⏱ Time Spent:** 1.5 hours  
**📄 Script:** `step_1_2_missing_values.py`

#### Objective
Address missing values in **BOTH training and test datasets** using identical preprocessing logic to ensure consistency for future predictions. Missing data can significantly impact model performance.

#### Missing Value Analysis

**Training Dataset:**
- MarkDown1: 270,889 missing (64.3%)
- MarkDown2: 310,322 missing (73.6%)
- MarkDown3: 284,479 missing (67.5%)
- MarkDown4: 286,603 missing (68.0%)
- MarkDown5: 270,138 missing (64.1%)
- Other columns: Complete ✓

**Test Dataset:**
- Similar missing pattern in MarkDown columns (64-74%)
- Other columns: Complete ✓

**Interpretation:** Missing values represent weeks WITHOUT promotional markdowns - this is expected business behavior, not data quality issues.

#### Strategy Implemented

**Approach: Dual Strategy for MarkDown Columns**

1. **Fill with 0** (no promotion that week)
   - Mathematically correct: $0 markdown means no promotion
   - Preserves the continuous nature of the variable
   
2. **Create Binary Indicators** (Has_MarkDownX)
   - Value 1: Promotion was active that week
   - Value 0: No promotion
   - Allows models to learn "promotion presence" as separate feature

**Why Both?**
- Amount matters: $100 vs $10,000 markdown has different impact
- Presence matters: Having ANY promotion vs none can signal strategic timing
- Model flexibility: Tree-based models can use both effectively

#### Implementation Results

**Training Dataset:**
- Before: 421,570 rows × 16 columns | Missing: 1,422,431
- After: 421,570 rows × 21 columns | Missing: 0 (100% complete)
- New columns: 5 binary indicators (Has_MarkDown1-5)

**Test Dataset:**
- Before: 115,064 rows × 15 columns | Missing: ~400,000
- After: 115,064 rows × 20 columns | Missing: 0 (100% complete)
- New columns: 5 binary indicators (Has_MarkDown1-5)

**Critical Achievement:** Both datasets now have IDENTICAL feature structure (except train has Weekly_Sales target)

**New Columns Created:**
| Column | Description | Values | Percentage with Promotion |
|--------|-------------|--------|---------------------------|
| Has_MarkDown1 | MarkDown1 present | 0 or 1 | 35.7% |
| Has_MarkDown2 | MarkDown2 present | 0 or 1 | 26.4% |
| Has_MarkDown3 | MarkDown3 present | 0 or 1 | 32.5% |
| Has_MarkDown4 | MarkDown4 present | 0 or 1 | 32.0% |
| Has_MarkDown5 | MarkDown5 present | 0 or 1 | 35.9% |

#### MarkDown Statistics (After Cleaning)

| MarkDown | Mean | Median | Non-Zero % |
|----------|------|--------|------------|
| MarkDown1 | $2,590.07 | $0.00 | 35.7% |
| MarkDown2 | $879.97 | $0.00 | 26.0% |
| MarkDown3 | $468.09 | $0.00 | 32.4% |
| MarkDown4 | $1,083.13 | $0.00 | 32.0% |
| MarkDown5 | $1,662.77 | $0.00 | 35.9% |

**Key Insight:** About 26-36% of weeks have promotional markdowns, confirming these are strategic, not constant.

#### Sample Data Example

Store 1, Dept 1 - First 10 weeks:
```
Date       | MarkDown1 | Has_MarkDown1 | Weekly_Sales
2010-02-05 |      0.00 |             0 |    24,924.50
2010-02-12 |      0.00 |             0 |    46,039.49
2010-02-19 |      0.00 |             0 |    41,595.55
... (all showing 0 markdowns in early weeks)
```

#### Data Persistence

**Output Files:**

1. **Training Data:** `processed_data/train_cleaned_step2.csv`
   - Size: ~38 MB
   - Rows: 421,570
   - Columns: 21
   - Quality: 100% complete (0 missing values)

2. **Test Data:** `processed_data/test_cleaned_step2.csv`
   - Size: ~11 MB
   - Rows: 115,064
   - Columns: 20
   - Quality: 100% complete (0 missing values)

#### Results Summary

✅ **Achievements:**
1. Analyzed missing value patterns in both datasets (64-74% in MarkDowns)
2. Implemented dual strategy: fill + binary indicators
3. Created 5 new feature columns in each dataset
4. Achieved 100% data completeness in both datasets
5. Preserved original data integrity
6. **Ensured train-test preprocessing consistency**

📊 **Impact:**
- Both datasets ready for modeling (no missing values)
- Added 5 new predictive features to each
- Maintained business logic interpretation
- No data loss (all rows retained in both datasets)
- Identical preprocessing ensures valid predictions

🔑 **Key Success:** Train and test datasets now have matching feature structures, ensuring:
- Model trained on train data can predict on test data
- No feature mismatch errors during prediction
- Consistent interpretation across datasets

#### Next Steps

🔜 **Step 1.3:** Outlier Detection
- Analyze negative sales (returns/clearances)
- Detect extreme values using IQR method
- Decision on treatment strategy

---

### Step 1.3: Outlier Detection

**📅 Status:** Pending  
**📄 Script:** `step_1_3_outliers.py` (to be created)

*To be completed...*

---

### Step 1.4: Feature Engineering

**📅 Status:** Pending  
**📄 Script:** `step_1_4_feature_engineering.py` (to be created)

*To be completed...*

---

### Step 1.5: Encoding Categorical Features

**📅 Status:** Pending  
**📄 Script:** `step_1_5_encoding.py` (to be created)

*To be completed...*

---

## 📝 Development Log

### October 23, 2025
- ✅ **Completed Step 1.1:** Data Loading & Merging
  - Loaded 4 datasets successfully
  - Merged train + stores + features
  - Created unified dataset (421,570 records)
  - Identified missing value patterns
  - Saved processed data to `processed_data/`

- ✅ **Completed Step 1.2:** Handling Missing Values (Train & Test)
  - Analyzed MarkDown columns in both datasets (64-74% missing)
  - Implemented dual strategy: fill with 0 + binary indicators
  - Created 5 new feature columns (Has_MarkDown1-5) in each dataset
  - Achieved 100% data completeness in both datasets
  - Ensured train-test preprocessing consistency
  - Saved cleaned data: `train_cleaned_step2.csv` + `test_cleaned_step2.csv`

---

## 📈 Progress Tracker

### Milestone 1: Data Collection & Preprocessing
- [x] Step 1.1: Data Loading & Merging ✅
- [x] Step 1.2: Handling Missing Values ✅
- [ ] Step 1.3: Outlier Detection
- [ ] Step 1.4: Feature Engineering
- [ ] Step 1.5: Encoding Categorical Features

### Milestone 2: Data Analysis & Visualization
- [ ] Not started

### Milestone 3: Model Development
- [ ] Not started

### Milestone 4: Deployment & Monitoring
- [ ] Not started

### Milestone 5: Final Documentation & Presentation
- [ ] Not started

**Overall Progress:** 12% (2/17 steps completed)

**Note:** Step 1.2 processes BOTH train and test datasets to ensure consistency.

---

## 🔧 Technical Stack

- **Python Version:** 3.12
- **Core Libraries:**
  - pandas (data manipulation)
  - numpy (numerical operations)
  - openpyxl (Excel file reading)
- **To be added:** scikit-learn, matplotlib, seaborn, xgboost, etc.

---

## 📁 Project Structure

```
Depi_project_Data-science/
├── datasets/
│   └── walmart-recruiting-store-sales-forecasting/
│       ├── train.csv
│       ├── test.csv
│       ├── stores.csv
│       └── features.xlsx
├── processed_data/
│   ├── train_merged.csv           ✅ Step 1.1 output
│   ├── test_merged.csv            ✅ Step 1.1 output
│   ├── train_cleaned_step2.csv    ✅ Step 1.2 output (421,570 rows × 21 cols)
│   └── test_cleaned_step2.csv     ✅ Step 1.2 output (115,064 rows × 20 cols)
├── step_1_1_data_loading_merging.py    ✅ Completed
├── step_1_2_missing_values.py          ✅ Completed (handles both train & test)
├── DOCUMENTATION.md                     ✅ Main documentation
├── PROJECT_SUMMARY.md                   ✅ Progress summary
├── main.py
└── README.md
```

---

## 📞 Contact & Notes

**Questions or Issues?**
- Document any blockers or questions here
- Keep track of decisions made and their rationale

---

*This documentation is updated continuously as the project progresses.*  
*Last Updated: October 23, 2025*

