# 🛒 Walmart Sales Forecasting Project

**AI & Data Science Track - Round 2**  
**Project Type:** Time Series Forecasting  
**Dataset:** Walmart Recruiting Store Sales Forecasting (Kaggle)  
**Status:** Milestone 1 Complete (85%) - Ready for Model Development

---

## 📋 Project Overview

This project develops a machine learning system to forecast weekly sales for Walmart stores across 45 locations and 99 departments. The goal is to predict future sales using historical data, store characteristics, external factors, and promotional activities.

### 🎯 Business Objectives

- **Inventory Optimization**: Prevent stockouts and overstocking
- **Staff Scheduling**: Allocate resources based on predicted demand
- **Marketing Planning**: Time promotions for maximum impact
- **Financial Forecasting**: Accurate revenue projections

### 📊 Success Metrics

- **MAE (Mean Absolute Error)**: < $3,000 per week
- **RMSE (Root Mean Square Error)**: < $5,000 per week
- **MAPE (Mean Absolute Percentage Error)**: < 15%
- **Baseline Improvement**: Beat naive forecasting by 25%+

---

## 📁 Dataset Summary

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

## 🎯 Project Milestones

### ✅ Milestone 1: Data Collection, Exploration & Preprocessing (85% Complete)

**Completed:**
- ✅ **Task 1: Data Collection** - Acquired and merged 4 datasets
- ✅ **Task 2: Data Exploration** - EDA with 10 visualizations, missing value analysis
- ✅ **Task 3: Feature Engineering** - 20 time features, 7 lag features, encoding, normalization
- ✅ **Task 4: EDA** - Comprehensive analysis with actionable insights

**Deliverables:**
- ✅ Cleaned Dataset (100%): `processed_data/Final/train_final.csv` & `test_final.csv`
- ✅ Interactive Visualizations (100%): 10 professional visualizations
- 🟡 EDA Report (85%): Analysis complete, formal writeup pending

### ⏳ Milestone 2: Model Development (Next Phase)

- Build baseline models (naive forecasting)
- Train advanced models (Random Forest, XGBoost, LSTM)
- Hyperparameter tuning
- Model evaluation and comparison

### ⏳ Milestone 3: Model Evaluation & Selection

- Cross-validation for time series
- Performance metrics analysis
- Best model selection
- Error analysis

### ⏳ Milestone 4: Deployment & Monitoring

- Deploy model (Flask/Streamlit)
- Create prediction API
- Set up monitoring for drift
- Production testing

### ⏳ Milestone 5: Final Documentation & Presentation

- Final report
- Presentation slides
- Code documentation
- Deployment guide

---

## 🔑 Key Insights from EDA

### 📈 Seasonality (Critical!)
- **Q4 sales are 35-40% higher than Q1** - Strong holiday surge
- November and December are peak months
- Models must capture seasonal patterns

### 🎉 Holiday Impact
- **+11.6% sales lift** during holiday weeks
- Consistent across all store types
- IsHoliday is a strong predictor

### 💰 Promotion Effectiveness
- **All markdowns increase sales** (positive ROI)
- MarkDown5: +22.1% lift (most effective)
- MarkDown1: +18.9% lift (second best)
- Promotion features are valuable predictors

### 🏪 Store Types
- **Type A (Large)**: 55% of sales, highest variance
- **Type B (Medium)**: 30% of sales, stable performance
- **Type C (Small)**: 15% of sales, most consistent
- Store type segmentation is critical

### 📊 External Factors
- **Unemployment**: Strongest correlation (-0.128)
- Temperature, Fuel Price: Minimal impact
- CPI: Moderate correlation

### 🎯 Department Concentration
- **Top 10 departments = 66% of total sales**
- Power law distribution suggests focused forecasting

---

## 🛠️ Technical Stack

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

## 📂 Project Structure

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
│   └── Final/                         # ⭐ READY FOR MODELING
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
├── DOCUMENTATION.md                   # 📘 Complete project documentation
├── README.md                          # 📄 This file
└── main.py                           # Initial exploration script
```

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### Running the Pipeline

**Step 1: Data Loading**
```bash
python step_1_1_data_loading_merging.py
```

**Step 2: Handle Missing Values**
```bash
python step_1_2_missing_values.py
```

**Step 3: Feature Engineering**
```bash
python step_1_3_1_time_features.py
python step_1_3_2_lag_features.py
python step_1_3_3_encode_categorical.py
python step_1_3_4_normalize_features_final.py
```

**Step 4: Exploratory Data Analysis**
```bash
python step_1_4_eda_analysis.py
```

### Loading Final Data
```python
import pandas as pd

# Load modeling-ready data
train = pd.read_csv('processed_data/Final/train_final.csv')
test = pd.read_csv('processed_data/Final/test_final.csv')

print(f"Train: {train.shape}")  # (421570, 49)
print(f"Test: {test.shape}")    # (115064, 48)

# Features are normalized, encoded, and ready for ML!
```

---

## 🔄 Data Generation Pipeline

### **Option 1: Automated Pipeline (RECOMMENDED)**

Run the complete feature engineering pipeline in one command:

```bash
python feature_engineering_pipeline.py
```

**⏱️ Execution Time:** ~60 seconds  
**💾 Total Output:** ~506 MB of processed data

#### What Gets Generated:

```
processed_data/
│
├── Stage1.3.1/                    # After Time Features
│   ├── train_time_features.csv    # 421,570 × 40 cols (~180 MB)
│   └── test_time_features.csv     # 115,064 × 39 cols (~48 MB)
│
├── Stage1.3.2/                    # After Lag Features
│   ├── train_lag_features.csv     # 421,570 × 47 cols (~210 MB)
│   └── test_lag_features.csv      # 115,064 × 46 cols (~56 MB)
│
├── Stage1.3.3/                    # After Encoding
│   ├── train_encoded.csv          # 421,570 × 49 cols (~223 MB)
│   └── test_encoded.csv           # 115,064 × 48 cols (~60 MB)
│
└── Final/                         # ⭐ FINAL OUTPUT
    ├── train_final.csv            # 421,570 × 49 cols (~223 MB)
    ├── test_final.csv             # 115,064 × 48 cols (~60 MB)
    └── normalization_params.json  # Normalization parameters (1.5 KB)
```

#### Pipeline Stages:

**Stage 1.3.1: Time-Based Features (19 features)**
- ✅ Year, Month, Day, Quarter, DayOfWeek, WeekOfYear
- ✅ Binary: Is_Weekend, Is_Month_Start/End, Is_Quarter_Start/End, Is_Year_Start/End
- ✅ Cyclical: Month_Sin/Cos, Week_Sin/Cos, DayOfWeek_Sin/Cos
- 📊 Output: 40 columns (train) | 39 columns (test)

**Stage 1.3.2: Lag Features (7 features)**
- ✅ Sales_Lag1, Sales_Lag2, Sales_Lag4
- ✅ Sales_Rolling_Mean_4, Sales_Rolling_Mean_8
- ✅ Sales_Rolling_Std_4, Sales_Momentum
- 📊 Output: 47 columns (train) | 46 columns (test)

**Stage 1.3.3: Categorical Encoding (3 features)**
- ✅ Type → Type_A, Type_B, Type_C (One-Hot Encoding)
- 📊 Output: 49 columns (train) | 48 columns (test)

**Stage 1.3.4: Numerical Normalization (17 features)**
- ✅ Z-score normalization: (X - μ) / σ
- ✅ Features: Size, Temperature, Fuel_Price, CPI, Unemployment, MarkDown1-5, All lag features
- 📊 Output: 49 columns (train) | 48 columns (test)

#### Console Output:

```
================================================================================
🚀 FEATURE ENGINEERING PIPELINE
================================================================================

⏰ STEP 1.3.1: CREATING TIME-BASED FEATURES
✅ Created 19 time-based features
💾 Saving Step 1.3.1 output...

📊 STEP 1.3.2: CREATING LAG FEATURES
✅ Created 7 lag features
💾 Saving Step 1.3.2 output...

🔤 STEP 1.3.3: ENCODING CATEGORICAL VARIABLES
✅ Encoded categorical variables
💾 Saving Step 1.3.3 output...

📐 STEP 1.3.4: NORMALIZING NUMERICAL FEATURES
✅ Normalization complete!
💾 Saving final datasets...

🎉 FEATURE ENGINEERING PIPELINE COMPLETE!
🚀 Ready for Model Development (Milestone 2)!
```

---

### **Option 2: Step-by-Step Execution**

If you need to run preprocessing before feature engineering or want more control:

#### Step 1: Data Loading & Merging
```bash
python step_1_1_data_loading_merging.py
```
**Output:** `processed_data/Stage1.1/train_merged.csv`, `test_merged.csv`

#### Step 2: Handle Missing Values
```bash
python step_1_2_missing_values.py
```
**Output:** `processed_data/Stage1.2/train_cleaned_step2.csv`, `test_cleaned_step2.csv`

#### Step 3: Feature Engineering (Individual Steps)
```bash
python step_1_3_1_time_features.py        # Time-based features
python step_1_3_2_lag_features.py         # Lag features
python step_1_3_3_encode_categorical.py   # Categorical encoding
python step_1_3_4_normalize_features_final.py  # Normalization
```

#### Step 4: Exploratory Data Analysis
```bash
python step_1_4_eda_analysis.py
```
**Output:** 10 visualizations in `visualizations/Stage1.4/`

---

### 📋 Verifying Generated Data

After running the pipeline, verify your data:

```bash
# Windows PowerShell
dir processed_data\Final

# Expected Output:
# train_final.csv          223 MB
# test_final.csv            60 MB
# normalization_params.json  1.5 KB
```

**Check data integrity:**
```python
import pandas as pd

train = pd.read_csv('processed_data/Final/train_final.csv')
test = pd.read_csv('processed_data/Final/test_final.csv')

print(f"Train shape: {train.shape}")  # Should be (421570, 49)
print(f"Test shape: {test.shape}")    # Should be (115064, 48)
print(f"Missing values (train): {train.isnull().sum().sum()}")  # Should be 0
print(f"Missing values (test): {test.isnull().sum().sum()}")    # Should be 0
print(f"Duplicates (train): {train.duplicated().sum()}")        # Should be 0
```

---

### 🎯 Which Data to Use?

| Purpose | Use This File | Reason |
|---------|---------------|---------|
| **Model Training & Testing** | `processed_data/Final/train_final.csv` & `test_final.csv` | ⭐ Fully processed, normalized, ready for ML |
| **Intermediate Analysis** | `processed_data/Stage1.3.X/` files | View data after specific transformation steps |
| **EDA / Visualization** | `processed_data/Stage1.2/` files | Original scale, easier to interpret |
| **Raw Data** | `datasets/walmart-recruiting-store-sales-forecasting/` | Unprocessed original datasets |

---

## 📊 Feature Engineering Pipeline

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

## 📈 Results & Insights

### Data Quality
- ✅ **0 missing values** (100% complete)
- ✅ **0 duplicates**
- ✅ **421,570 training examples**
- ✅ **49 engineered features**

### Patterns Discovered
- 📊 Strong seasonality (Q4 peak)
- 🎉 Consistent holiday lift (+11.6%)
- 💰 Effective promotions (up to +22% lift)
- 🏪 Clear store type differences
- 📉 Economic indicators matter (Unemployment -0.128 correlation)

### Data Readiness
- ✅ All preprocessing complete
- ✅ Features normalized (mean=0, std=1)
- ✅ Train-test consistency maintained
- ✅ No data leakage
- ✅ Production parameters saved

---

## 🎓 Key Learnings

1. **Seasonality is Dominant**: Q4 surge must be captured by models
2. **Holidays Matter**: Simple IsHoliday flag provides +11.6% predictive power
3. **Promotions Work**: All MarkDown types increase sales
4. **Store Segmentation**: Type A/B/C behave differently
5. **Lag Features Critical**: Historical sales are strong predictors
6. **Normalization Essential**: Features had vastly different scales

---

## 📝 Next Steps

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

## 👥 Team

**Data Science Team**  
**Project:** AI & Data Science Track - Round 2  
**Institution:** DEPI (Digital Egypt Pioneers Initiative)

---

## 📚 Documentation

For detailed implementation steps, code explanations, and complete analysis, see:
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Complete project documentation (55KB, comprehensive)

---

## 📧 Contact

For questions or collaboration:
- Project Repository: `D:\projects\Depi_project_Data-science`
- Last Updated: October 23, 2025

---

## ⚖️ License

This project is developed for educational purposes as part of the DEPI AI & Data Science Track.

---

**Status:** ✅ Milestone 1 Complete | 🚀 Ready for Model Development | 📊 Dataset: 421K training examples, 49 features
