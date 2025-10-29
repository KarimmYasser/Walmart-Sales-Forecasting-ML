# Stage 1: Data Preprocessing & Feature Engineering

**Status:** Complete  
**Date Completed:** October 24, 2025

---

## Objectives

Collect, explore, clean, and prepare sales data for forecasting through comprehensive preprocessing and feature engineering.

---

## Tasks Completed

### Task 1.1: Data Loading & Merging
**Script:** `step_1_1_data_loading_merging.py`

**Deliverables:**
- Merged training and test datasets with store and feature data
- `processed_data/Stage1.1/train_merged.csv` (421,570 rows × 20 cols)
- `processed_data/Stage1.1/test_merged.csv` (115,064 rows × 19 cols)

### Task 1.2: Missing Values & Data Quality
**Script:** `step_1_2_missing_values.py`

**Key Actions:**
- Handled MarkDown columns (64-74% missing) - filled with 0 + binary indicators
- Created 5 promotion indicator features (Has_MarkDown1-5)
- Achieved 100% data completeness

**Deliverables:**
- `processed_data/Stage1.2/train_cleaned_step2.csv` (421,570 rows × 25 cols)
- `processed_data/Stage1.2/test_cleaned_step2.csv` (115,064 rows × 24 cols)

### Task 1.3: Outlier Detection (Optional)
**Script:** `step_1_3_outlier_detection.py`

**Deliverables:**
- 4 outlier analysis visualizations
- Statistical outlier analysis using IQR method
- Decision: Retained all outliers (valid business scenarios)

### Task 1.4: Exploratory Data Analysis
**Script:** `step_1_4_eda_analysis.py`

**Deliverables:**
- 10 comprehensive visualizations in `visualizations/Stage1.4/`
- Key insights: Q4 peak (+35-40%), holiday lift (+11.6%), promotion effectiveness

### Task 1.3.1-1.3.4: Feature Engineering Pipeline
**Scripts:** 
- `step_1_3_1_time_features.py` - 20 time-based features
- `step_1_3_2_lag_features.py` - 7 lag and rolling features
- `step_1_3_3_encode_categorical.py` - 3 categorical encodings
- `step_1_3_4_normalize_features_final.py` - Normalized 17 features

**Deliverables:**
- `processed_data/Stage1.3.4_Final/train_final.csv` (421,570 rows × 54 features)
- `processed_data/Stage1.3.4_Final/test_final.csv` (115,064 rows × 53 features)
- `processed_data/Stage1.3.4_Final/normalization_params.json`

---

## Folder Structure

```
stage1/
├── step_1_1_data_loading_merging.py      # Data collection & merging
├── step_1_2_missing_values.py            # Missing value handling
├── step_1_3_outlier_detection.py         # Outlier analysis (optional)
├── step_1_4_eda_analysis.py              # EDA visualizations
├── step_1_3_1_time_features.py           # Time-based features
├── step_1_3_2_lag_features.py            # Lag and rolling features
├── step_1_3_3_encode_categorical.py      # Categorical encoding
├── step_1_3_4_normalize_features_final.py# Feature normalization
├── Stage1_pipline_runner.py              # One-click pipeline execution
├── README.md                              # This file
│
├── processed_data/
│   ├── Stage1.1/                         # Merged data
│   ├── Stage1.2/                         # Cleaned data
│   ├── Stage1.3.1/                       # Time features added
│   ├── Stage1.3.2/                       # Lag features added
│   ├── Stage1.3.3/                       # Categorical encoded
│   └── Stage1.3.4_Final/                 # READY FOR MODELING
│       ├── train_final.csv               # 421,570 × 54
│       ├── test_final.csv                # 115,064 × 53
│       └── normalization_params.json     # Scaling parameters
│
├── visualizations/
│   ├── Stage1.3/                         # Outlier detection (4 plots)
│   └── Stage1.4/                         # EDA analysis (10 plots)
│
└── Milestone_1_Deliverables/             # Formal deliverables
    ├── EDA_Analysis_notebook/
    │   └── EDA_Analysis.ipynb
    └── EDA-REPORT/
        ├── EDA_REPORT.md
        ├── EDA-Report.pdf
        └── EDA.docx
```

---

## How to Run

### Prerequisites

**Ensure raw data exists:**
- `../Datasets/walmart-recruiting-store-sales-forecasting/train.csv`
- `../Datasets/walmart-recruiting-store-sales-forecasting/test.csv`
- `../Datasets/walmart-recruiting-store-sales-forecasting/stores.csv`
- `../Datasets/walmart-recruiting-store-sales-forecasting/features.xlsx`

**From project root:**
```bash
cd stage1
```

---

### Option 1: One-Click Pipeline (Recommended)

```bash
# From stage1/ directory
python Stage1_pipline_runner.py
```

**This will automatically execute:**
1. Step 1.3.1: Time-Based Features
2. Step 1.3.2: Lag Features  
3. Step 1.3.3: Categorical Encoding
4. Step 1.3.4: Normalization

**Note:** This pipeline assumes Steps 1.1 and 1.2 have already been run (data exists in `processed_data/Stage1.2/`)

**Execution Time:** ~1-2 minutes  
**Output:** `processed_data/Stage1.3.4_Final/` with modeling-ready datasets

---

### Option 2: Step-by-Step Execution

If you want to understand each step or need to start from the beginning:

#### Phase 1: Data Preparation

**Step 1.1: Load and Merge Datasets**
```bash
python step_1_1_data_loading_merging.py
```
- **Input:** `../Datasets/walmart-recruiting-store-sales-forecasting/`
- **Output:** `processed_data/Stage1.1/` (merged datasets)
- **Time:** ~5-10 seconds

**Step 1.2: Handle Missing Values**
```bash
python step_1_2_missing_values.py
```
- **Input:** `processed_data/Stage1.1/`
- **Output:** `processed_data/Stage1.2/` (100% complete data)
- **Time:** ~3-5 seconds

**Step 1.3: Outlier Detection (Optional)**
```bash
python step_1_3_outlier_detection.py
```
- **Input:** `processed_data/Stage1.2/train_cleaned_step2.csv`
- **Output:** `visualizations/Stage1.3/` (4 plots)
- **Time:** ~10-15 seconds

**Step 1.4: EDA Analysis (Optional but Recommended)**
```bash
python step_1_4_eda_analysis.py
```
- **Input:** `processed_data/Stage1.2/train_cleaned_step2.csv`
- **Output:** `visualizations/Stage1.4/` (10 plots)
- **Time:** ~15-20 seconds

#### Phase 2: Feature Engineering

**Step 1.3.1: Create Time-Based Features**
```bash
python step_1_3_1_time_features.py
```
- **Features Added:** 20 (Year, Month, Quarter, cyclical encodings, etc.)
- **Output:** `processed_data/Stage1.3.1/`
- **Time:** ~3-5 seconds

**Step 1.3.2: Create Lag Features**
```bash
python step_1_3_2_lag_features.py
```
- **Features Added:** 7 (Sales_Lag1/2/4, rolling means/std, momentum)
- **Output:** `processed_data/Stage1.3.2/`
- **Time:** ~8-12 seconds

**Step 1.3.3: Encode Categorical Variables**
```bash
python step_1_3_3_encode_categorical.py
```
- **Features Added:** 3 (Type_A, Type_B, Type_C via one-hot encoding)
- **Output:** `processed_data/Stage1.3.3/`
- **Time:** ~2-3 seconds

**Step 1.3.4: Normalize Features**
```bash
python step_1_3_4_normalize_features_final.py
```
- **Features Normalized:** 17 (Z-score standardization)
- **Output:** `processed_data/Stage1.3.4_Final/` (READY FOR MODELING)
- **Time:** ~3-5 seconds

---

## Key Features Created

### 1. Time-Based Features (20)
- **Basic:** Year, Month, Day, Quarter, DayOfWeek, WeekOfYear
- **Binary Indicators:** Is_Weekend, Is_Month_Start/End, Is_Quarter_Start/End, Is_Year_Start/End
- **Cyclical Encodings:** Month_Sin/Cos, Week_Sin/Cos, DayOfWeek_Sin/Cos

### 2. Lag & Rolling Features (7)
- **Lag Features:** Sales_Lag1, Sales_Lag2, Sales_Lag4
- **Rolling Statistics:** Sales_Rolling_Mean_4, Sales_Rolling_Mean_8, Sales_Rolling_Std_4
- **Momentum:** Sales_Momentum (week-over-week change)

### 3. Categorical Encoding (3)
- **Store Type:** Type_A, Type_B, Type_C (one-hot encoded)

### 4. Promotion Indicators (5)
- **Binary Flags:** Has_MarkDown1, Has_MarkDown2, Has_MarkDown3, Has_MarkDown4, Has_MarkDown5

### 5. Normalized Features (17)
- **Continuous Variables:** Size, Temperature, Fuel_Price, CPI, Unemployment, MarkDown1-5, all lag features
- **Method:** Z-score normalization (mean=0, std=1)

**Total Features:** 54 (train), 53 (test)

---

## Key Insights from EDA

### Seasonality (Critical)
- **Q4 dominance:** Nov-Dec sales are 35-40% higher than Q1
- **Monthly patterns:** Clear peaks in November and December
- **Models must capture:** Strong seasonal effects

### Holiday Impact
- **+11.6% sales lift** during holiday weeks
- Consistent across all store types
- IsHoliday is a strong predictor

### Promotion Effectiveness
- **All markdowns increase sales** (9-22% lift)
- MarkDown5: +22.1% lift (most effective)
- MarkDown1: +18.9% lift (second best)

### Store Type Performance
- **Type A (Large):** 55% of sales, highest variance
- **Type B (Medium):** 30% of sales, stable
- **Type C (Small):** 15% of sales, most consistent

### External Factors
- **Unemployment:** Strongest correlation (-0.128)
- **Temperature:** Weak positive correlation (+0.065)
- **Fuel Price/CPI:** Minimal direct impact

### Department Concentration
- **Top 10 departments:** 66% of total sales
- Power law distribution suggests focused forecasting

---

## Data Quality Metrics

**Final Dataset Statistics:**
- **Missing Values:** 0 (100% complete)
- **Duplicates:** 0
- **Training Samples:** 421,570
- **Test Samples:** 115,064
- **Feature Count:** 54 (train), 53 (test)
- **Normalized Features:** 17
- **Binary Features:** 13
- **Cyclical Features:** 6

**Data Integrity:**
- All preprocessing applied identically to train and test
- Normalization parameters saved for production consistency
- No data leakage (test statistics never used in train processing)
- Temporal ordering preserved for lag features

---

## Verify Generated Data

**Check files exist:**
```bash
# Windows
dir processed_data\Stage1.3.4_Final

# Linux/Mac
ls -lh processed_data/Stage1.3.4_Final/
```

**Expected output:**
```
train_final.csv           ~57 MB
test_final.csv            ~16 MB
normalization_params.json ~1.5 KB
```

**Verify data integrity (Python):**
```python
import pandas as pd

# Load final datasets
train = pd.read_csv('processed_data/Stage1.3.4_Final/train_final.csv')
test = pd.read_csv('processed_data/Stage1.3.4_Final/test_final.csv')

# Check shapes
print(f"Train shape: {train.shape}")  # Should be (421570, 54)
print(f"Test shape: {test.shape}")    # Should be (115064, 53)

# Check data quality
print(f"Missing values (train): {train.isnull().sum().sum()}")  # Should be 0
print(f"Missing values (test): {test.isnull().sum().sum()}")    # Should be 0

# Verify normalization
continuous_features = ['Size', 'Temperature', 'CPI', 'Sales_Lag1']
print(f"\nNormalized features (mean ~0):")
print(train[continuous_features].mean())
print(f"\nNormalized features (std ~1):")
print(train[continuous_features].std())
```

---

## Loading Data for Modeling

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

# Separate features and target
X_train = train.drop(['Weekly_Sales', 'Date'], axis=1)
y_train = train['Weekly_Sales']
X_test = test.drop(['Date'], axis=1)

print(f"\nX_train: {X_train.shape}")  # (421570, 52)
print(f"y_train: {y_train.shape}")    # (421570,)
print(f"X_test: {X_test.shape}")      # (115064, 52)
```

---

## Next Steps

### Stage 2: Advanced Analysis
After completing Stage 1, proceed to Stage 2 for enhanced feature engineering:

```bash
cd ../stage2
python Stage2_pipline_runner.py
```

**Stage 2 will add:**
- 42 additional enhanced features
- Advanced time series analysis
- 10 advanced visualizations
- Comprehensive analysis reports

### Model Development
With Stage 1 (or Stage 2) complete, proceed to model development:

1. **Baseline Models:** Naive forecasting, moving average
2. **ML Models:** Random Forest, XGBoost, LightGBM
3. **Time Series Models:** ARIMA, Prophet
4. **Deep Learning:** LSTM, GRU

---

## Documentation

**Main Documentation:**
- **[EDA Report](Milestone_1_Deliverables/EDA-REPORT/EDA_REPORT.md)** - Complete EDA findings
- **[EDA Notebook](Milestone_1_Deliverables/EDA_Analysis_notebook/EDA_Analysis.ipynb)** - Interactive analysis

**Code Documentation:**
- Each script contains detailed inline comments
- Function docstrings explain parameters and returns
- Step-by-step processing logic documented

---

## Recommendations for Model Training

Based on Stage 1 analysis:

### Must-Include Features
- Lag features (Lag1, Lag2, Lag4)
- Rolling means (4-week, 8-week)
- Time features (Month, Quarter, cyclical)
- Holiday indicator
- Store Type
- Promotion indicators

### Should-Include Features
- Store size
- Unemployment rate
- Temperature
- All engineered features

### Consider Excluding
- Fuel_Price (minimal correlation)
- Individual markdown amounts (use indicators instead)

### Modeling Strategy
1. Start with simple models using critical features only
2. Gradually add feature groups and measure impact
3. Consider store-type-specific models
4. Use time-series cross-validation
5. Ensemble multiple models for robustness

---

**Last Updated:** October 29, 2025  
**Version:** 1.0  
**License:** MIT
