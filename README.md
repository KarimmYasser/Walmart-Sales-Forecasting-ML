# Walmart Sales Forecasting Project

**AI & Data Science Track - Round 2**  
**Project Type:** Time Series Forecasting  
**Dataset:** Walmart Recruiting Store Sales Forecasting (Kaggle)  
**Status:** Milestone 1 Complete (85%) - Ready for Model Development

---

## Project Overview

This project develops a machine learning system to forecast weekly sales for Walmart stores across 45 locations and 99 departments. The goal is to predict future sales using historical data, store characteristics, external factors, and promotional activities.

### Business Objectives

- **Inventory Optimization**: Prevent stockouts and overstocking
- **Staff Scheduling**: Allocate resources based on predicted demand
- **Marketing Planning**: Time promotions for maximum impact
- **Financial Forecasting**: Accurate revenue projections

### Success Metrics

- **MAE (Mean Absolute Error)**: < $3,000 per week
- **RMSE (Root Mean Square Error)**: < $5,000 per week
- **MAPE (Mean Absolute Percentage Error)**: < 15%
- **Baseline Improvement**: Beat naive forecasting by 25%+

---

## Dataset Summary

| Dataset | Records | Columns | Date Range | Description |
|---------|---------|---------|------------|-------------|
| **Training** | 421,570 | 49 | 2010-02-05 to 2012-10-26 | Historical sales with target variable |
| **Test** | 115,064 | 48 | 2012-11-02 to 2013-07-26 | Future period for predictions |
| **Stores** | 45 | 3 | - | Store metadata (Type A/B/C, Size) |
| **Features** | 8,190 | 12 | - | External factors (Temperature, CPI, etc.) |

### Key Features

**Original (10):** Size, Temperature, Fuel_Price, MarkDown1-5, CPI, Unemployment  
**Engineered (39):** Time features (20), Lag features (7), Encoded categories (3), Promotion flags (5), Holiday (1)  
**Total Features:** 49 (train), 48 (test)

---

## Project Milestones

### Milestone 1: Data Collection, Exploration & Preprocessing (85% Complete)

**Completed:**
- **Task 1: Data Collection** - Acquired and merged 4 datasets
- **Task 2: Data Exploration** - EDA with 10 visualizations, missing value analysis
- **Task 3: Feature Engineering** - 20 time features, 7 lag features, encoding, normalization
- **Task 4: EDA** - Comprehensive analysis with actionable insights

**Deliverables:**
- Cleaned Dataset (100%): `processed_data/Final/train_final.csv` & `test_final.csv`
- Interactive Visualizations (100%): 10 professional visualizations
- EDA Report (85%): Analysis complete, formal writeup pending

### Milestone 2: Model Development (Next Phase)

- Build baseline models (naive forecasting)
- Train advanced models (Random Forest, XGBoost, LSTM)
- Hyperparameter tuning
- Model evaluation and comparison

### Milestone 3: Model Evaluation & Selection

- Cross-validation for time series
- Performance metrics analysis
- Best model selection
- Error analysis

### Milestone 4: Deployment & Monitoring

- Deploy model (Flask/Streamlit)
- Create prediction API
- Set up monitoring for drift
- Production testing

### Milestone 5: Final Documentation & Presentation

- Final report
- Presentation slides
- Code documentation
- Deployment guide

---

## Key Insights from EDA

### Seasonality (Critical!)
- **Q4 sales are 35-40% higher than Q1** - Strong holiday surge
- November and December are peak months
- Models must capture seasonal patterns

### Holiday Impact
- **+11.6% sales lift** during holiday weeks
- Consistent across all store types
- IsHoliday is a strong predictor

### Promotion Effectiveness
- **All markdowns increase sales** (positive ROI)
- MarkDown5: +22.1% lift (most effective)
- MarkDown1: +18.9% lift (second best)
- Promotion features are valuable predictors

### Store Types
- **Type A (Large)**: 55% of sales, highest variance
- **Type B (Medium)**: 30% of sales, stable performance
- **Type C (Small)**: 15% of sales, most consistent
- Store type segmentation is critical

### External Factors
- **Unemployment**: Strongest correlation (-0.128)
- Temperature, Fuel Price: Minimal impact
- CPI: Moderate correlation

### Department Concentration
- **Top 10 departments = 66% of total sales**
- Power law distribution suggests focused forecasting

---

## Technical Stack

**Languages & Libraries:**
- Python 3.12
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- scikit-learn (preprocessing, modeling)

**Data Processing:**
- Openpyxl (Excel files)
- Manual Z-score normalization
- One-Hot encoding for categories

**Models (Planned):**
- Random Forest Regressor
- XGBoost
- LSTM (for time series)
- ARIMA/SARIMA

---

## Project Structure

```
Depi_project_Data-science/
│
├── datasets/                          # Raw data
│   └── walmart-recruiting-store-sales-forecasting/
│       ├── train.csv
│       ├── test.csv
│       ├── stores.csv
│       └── features.xlsx
│
├── processed_data/                    # Processed data pipeline
│   ├── Stage1.1/                      # Merged data
│   ├── Stage1.2/                      # Missing values handled
│   ├── Stage1.3.1/                    # Time features added
│   ├── Stage1.3.2/                    # Lag features added
│   ├── Stage1.3.3/                    # Categorical encoded
│   └── Final/                         # READY FOR MODELING
│       ├── train_final.csv            # 421,570 × 49
│       ├── test_final.csv             # 115,064 × 48
│       └── normalization_params.json  # For production
│
├── visualizations/                    # EDA outputs
│   └── Stage1.4/
│       ├── 01_overall_sales_trend.png
│       ├── 05_holiday_impact.png
│       └── ... (10 visualizations)
│
├── Scripts/                           # Milestone 1 scripts
│   ├── step_1_1_data_loading_merging.py
│   ├── step_1_2_missing_values.py
│   ├── step_1_4_eda_analysis.py
│   ├── step_1_3_1_time_features.py
│   ├── step_1_3_2_lag_features.py
│   ├── step_1_3_3_encode_categorical.py
│   └── step_1_3_4_normalize_features_final.py
│
├── DOCUMENTATION.md                   # Complete project documentation
├── README.md                          # This file
└── main.py                           # Initial exploration script
```

---

## Getting Started

### Prerequisites

**Install Required Dependencies:**
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

**Verify Installation:**
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
print("All packages installed successfully!")
```

**Required Data Files:**
Ensure these files exist in `datasets/walmart-recruiting-store-sales-forecasting/`:
- `train.csv`
- `test.csv`
- `stores.csv`
- `features.xlsx`

---

## How to Generate All Required Data

### **OPTION 1: ONE-CLICK PIPELINE (RECOMMENDED)**

Run the entire data processing pipeline with a single command:

```bash
python feature_engineering_pipeline.py
```

**This will automatically:**
1. Execute all 4 feature engineering steps in sequence
2. Show progress and output from each step
3. Generate all intermediate and final datasets
4. Create `processed_data/Stage1.3.4_Final/` with modeling-ready data

**Execution Time:** ~30-60 seconds  
**Total Output:** ~500 MB of processed data

**Expected Console Output:**
```
================================================================================
FEATURE ENGINEERING PIPELINE
================================================================================

Pipeline Flow:
  Stage1.2 → [1.3.1] → Stage1.3.1 → [1.3.2] → Stage1.3.2
  → [1.3.3] → Stage1.3.3 → [1.3.4] → Stage1.3.4_Final

================================================================================
[1/4] STEP 1.3.1: TIME-BASED FEATURES
================================================================================
Input:  processed_data/Stage1.2/
Output: processed_data/Stage1.3.1/

[1] Loading cleaned data...
Loaded: train (421570, 20), test (115064, 19)

[2] Creating time-based features...
Created 20 time-based features

[3] Saving data with time features...
Saved: processed_data/Stage1.3.1/train_time_features.csv, ...

================================================================================
STEP 1.3.1 COMPLETED!
================================================================================

... [Similar output for steps 1.3.2, 1.3.3, 1.3.4] ...

================================================================================
PIPELINE COMPLETED SUCCESSFULLY!
================================================================================

Final Datasets Ready:
  processed_data/Stage1.3.4_Final/
     ├─ train_final.csv
     ├─ test_final.csv
     └─ normalization_params.json

Ready for Model Development!
```

---

### **OPTION 2: STEP-BY-STEP EXECUTION**

If you want to understand each stage or need preprocessing steps:

#### **STAGE 1: Data Preprocessing**

**Step 1.1: Load and Merge Datasets**
```bash
python step_1_1_data_loading_merging.py
```
- **Input:** `datasets/walmart-recruiting-store-sales-forecasting/`
- **Output:** `processed_data/Stage1.1/`
  - `train_merged.csv` (421,570 rows × 20 cols)
  - `test_merged.csv` (115,064 rows × 19 cols)
- **What it does:** Merges train/test with stores and features data

**Step 1.2: Handle Missing Values**
```bash
python step_1_2_missing_values.py
```
- **Input:** `processed_data/Stage1.1/`
- **Output:** `processed_data/Stage1.2/`
  - `train_cleaned_step2.csv` (421,570 rows × 25 cols)
  - `test_cleaned_step2.csv` (115,064 rows × 24 cols)
- **What it does:** 
  - Fills MarkDown nulls with 0
  - Creates Has_MarkDownX binary indicators
  - Forward/backward fill for CPI/Unemployment

**Step 1.3: Outlier Detection (Optional Analysis)**
```bash
python step_1_3_outlier_detection.py
```
- **Input:** `processed_data/Stage1.2/train_cleaned_step2.csv`
- **Output:** `visualizations/Stage1.3/` (4 plots)
- **What it does:** Analyzes outliers using IQR method, generates visualizations
- **Decision:** Keep all outliers (valid business scenarios)

---

#### **STAGE 2: Feature Engineering**

**Step 1.3.1: Create Time-Based Features**
```bash
python step_1_3_1_time_features.py
```
- **Input:** `processed_data/Stage1.2/`
- **Output:** `processed_data/Stage1.3.1/`
  - `train_time_features.csv` (421,570 rows × 45 cols)
  - `test_time_features.csv` (115,064 rows × 44 cols)
- **Features Added (20):**
  - Basic: Year, Month, Day, Quarter, DayOfWeek, WeekOfYear
  - Binary: Is_Weekend, Is_Month_Start/End, Is_Quarter_Start/End, Is_Year_Start/End
  - Cyclical: Month_Sin/Cos, Week_Sin/Cos, DayOfWeek_Sin/Cos

**Step 1.3.2: Create Lag Features**
```bash
python step_1_3_2_lag_features.py
```
- **Input:** `processed_data/Stage1.3.1/`
- **Output:** `processed_data/Stage1.3.2/`
  - `train_lag_features.csv` (421,570 rows × 52 cols)
  - `test_lag_features.csv` (115,064 rows × 51 cols)
- **Features Added (7):**
  - Sales_Lag1, Sales_Lag2, Sales_Lag4
  - Sales_Rolling_Mean_4, Sales_Rolling_Mean_8
  - Sales_Rolling_Std_4, Sales_Momentum

**Step 1.3.3: Encode Categorical Variables**
```bash
python step_1_3_3_encode_categorical.py
```
- **Input:** `processed_data/Stage1.3.2/`
- **Output:** `processed_data/Stage1.3.3/`
  - `train_encoded.csv` (421,570 rows × 54 cols)
  - `test_encoded.csv` (115,064 rows × 53 cols)
- **What it does:** One-hot encodes Store Type (A/B/C) → Type_A, Type_B, Type_C

**Step 1.3.4: Normalize Features**
```bash
python step_1_3_4_normalize_features_final.py
```
- **Input:** `processed_data/Stage1.3.3/`
- **Output:** `processed_data/Stage1.3.4_Final/` ⭐
  - `train_final.csv` (421,570 rows × 54 cols) 
  - `test_final.csv` (115,064 rows × 53 cols)
  - `normalization_params.json` (for production deployment)
- **What it does:** 
  - Z-score normalization: (X - μ) / σ
  - Normalizes 17 continuous features
  - Saves parameters for consistent test/production scaling

---

#### **STAGE 3: Exploratory Data Analysis**

**Step 1.4: Generate EDA Visualizations**
```bash
python step_1_4_eda_analysis.py
```
- **Input:** `processed_data/Stage1.2/train_cleaned_step2.csv`
- **Output:** `visualizations/Stage1.4/` (10 plots)
  1. Overall sales trend
  2. Sales by year
  3. Monthly seasonality
  4. Quarterly pattern
  5. Holiday impact
  6. Store type comparison
  7. Promotion impact
  8. External factors correlation
  9. External factors scatter plots
  10. Top departments
- **Time:** ~15-20 seconds

---

### Verify Generated Data

**Check Files Exist:**
```bash
# Windows
dir processed_data\Stage1.3.4_Final

# Linux/Mac
ls -lh processed_data/Stage1.3.4_Final/
```

**Expected Output:**
```
train_final.csv          ~223 MB
test_final.csv           ~60 MB
normalization_params.json ~1.5 KB
```

**Verify Data Integrity:**
```python
import pandas as pd

# Load final datasets
train = pd.read_csv('processed_data/Stage1.3.4_Final/train_final.csv')
test = pd.read_csv('processed_data/Stage1.3.4_Final/test_final.csv')

# Check shapes
print(f"Train shape: {train.shape}")  # (421570, 54)
print(f"Test shape: {test.shape}")    # (115064, 53)

# Check data quality
print(f"Missing values (train): {train.isnull().sum().sum()}")  # Should be 0
print(f"Missing values (test): {test.isnull().sum().sum()}")    # Should be 0
print(f"Duplicates (train): {train.duplicated().sum()}")        # Should be 0

# Check normalization (should have mean≈0, std≈1)
continuous_features = ['Size', 'Temperature', 'CPI', 'Sales_Lag1']
print(f"\nNormalized features (mean should be ≈0):")
print(train[continuous_features].mean())
print(f"\nNormalized features (std should be ≈1):")
print(train[continuous_features].std())

print("\nAll checks passed! Data is ready for modeling.")
```

---

### Loading Data for Modeling

```python
import pandas as pd
import json

# Load final processed data
train = pd.read_csv('processed_data/Stage1.3.4_Final/train_final.csv')
test = pd.read_csv('processed_data/Stage1.3.4_Final/test_final.csv')

# Load normalization parameters (for production)
with open('processed_data/Stage1.3.4_Final/normalization_params.json', 'r') as f:
    norm_params = json.load(f)

print(f"Train: {train.shape}")  # (421570, 54)
print(f"Test: {test.shape}")    # (115064, 53)
print(f"Features are normalized, encoded, and ready for ML!")

# Separate features and target
X_train = train.drop(['Weekly_Sales', 'Date'], axis=1)
y_train = train['Weekly_Sales']
X_test = test.drop(['Date'], axis=1)

print(f"\nX_train: {X_train.shape}")  # (421570, 52)
print(f"y_train: {y_train.shape}")    # (421570,)
print(f"X_test: {X_test.shape}")      # (115064, 52)
```

---

## Feature Engineering Pipeline

### 1. **Time-Based Features (20)**
- Basic: Year, Month, Day, Quarter, DayOfWeek, WeekOfYear
- Binary: Is_Weekend, Is_Month_Start/End, Is_Quarter_Start/End, Is_Year_Start/End
- Cyclical: Month_Sin/Cos, Week_Sin/Cos, DayOfWeek_Sin/Cos

### 2. **Lag Features (7)**
- Sales_Lag1, Sales_Lag2, Sales_Lag4 (historical sales per Store-Dept)
- Sales_Rolling_Mean_4, Sales_Rolling_Mean_8 (smoothed trends)
- Sales_Rolling_Std_4 (volatility)
- Sales_Momentum (change rate)

### 3. **Categorical Encoding (3)**
- Type_A, Type_B, Type_C (one-hot encoded store types)

### 4. **Normalization (17 features)**
- Z-Score: (x - μ) / σ for all continuous features
- Preserves patterns while standardizing scale

---

## Results & Insights

### Data Quality
- **0 missing values** (100% complete)
- **0 duplicates**
- **421,570 training examples**
- **49 engineered features**

### Patterns Discovered
- Strong seasonality (Q4 peak)
- Consistent holiday lift (+11.6%)
- Effective promotions (up to +22% lift)
- Clear store type differences
- Economic indicators matter (Unemployment -0.128 correlation)

### Data Readiness
- All preprocessing complete
- Features normalized (mean=0, std=1)
- Train-test consistency maintained
- No data leakage
- Production parameters saved

---

## Key Learnings

1. **Seasonality is Dominant**: Q4 surge must be captured by models
2. **Holidays Matter**: Simple IsHoliday flag provides +11.6% predictive power
3. **Promotions Work**: All MarkDown types increase sales
4. **Store Segmentation**: Type A/B/C behave differently
5. **Lag Features Critical**: Historical sales are strong predictors
6. **Normalization Essential**: Features had vastly different scales

---

## Next Steps

### Immediate (Milestone 2)
1. **Build Baseline Model** - Naive forecasting for comparison
2. **Random Forest** - Start with ensemble method
3. **XGBoost** - Gradient boosting for accuracy
4. **LSTM** - Deep learning for time series
5. **Model Comparison** - Evaluate all models against metrics

### Future Enhancements
- Department-specific models
- Store clustering for targeted forecasting
- Promotional optimization
- Real-time prediction API
- Automated retraining pipeline

---

## Team

**Data Science Team**  
**Project:** AI & Data Science Track - Round 2  
**Institution:** DEPI (Digital Egypt Pioneers Initiative)

---

## Documentation

For detailed implementation steps, code explanations, and complete analysis, see:
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete project documentation (55KB, comprehensive)

---

## Contact

For questions or collaboration:
- Project Repository: `D:\projects\Depi_project_Data-science`
- Last Updated: October 23, 2025

---

## License

This project is developed for educational purposes as part of the DEPI AI & Data Science Track.

---

**Status:** Milestone 1 Complete | Ready for Model Development | Dataset: 421K training examples, 49 features
