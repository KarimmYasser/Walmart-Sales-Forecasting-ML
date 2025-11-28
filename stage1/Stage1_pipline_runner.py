"""
Stage 1 Pipeline - Complete Data Processing & Feature Engineering
==================================================================
This script runs ALL Stage 1 tasks sequentially:
1. Data Loading & Merging
2. Missing Value Handling
3. Outlier Detection & Analysis
4. Feature Engineering (Time, Lag, Encoding, Normalization)
5. Exploratory Data Analysis (EDA)

IMPORTANT: Must be run from the project root directory.
"""

import os
import sys

# Get the stage1 directory path
stage1_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("STAGE 1 COMPLETE PIPELINE - DATA PROCESSING & FEATURE ENGINEERING")
print("="*70)
print("\nPipeline Flow:")
print("  [1.1] Data Loading → [1.2] Missing Values → [1.3] Outliers")
print("  → [1.3.1] Time Features → [1.3.2] Lag Features")
print("  → [1.3.3] Encoding → [1.3.4] Normalization → [1.4] EDA\n")
print("="*70)

# Step 1.1: Data Loading & Merging
print("\n[1/7] STEP 1.1: DATA LOADING & MERGING")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_1_data_loading_merging.py')}")
if exit_code != 0:
    print(f"\n❌ ERROR: Step 1.1 failed with exit code {exit_code}")
    sys.exit(1)
print("✅ Step 1.1 completed successfully!\n")

# Step 1.2: Missing Values
print("\n[2/7] STEP 1.2: HANDLING MISSING VALUES")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_2_missing_values.py')}")
if exit_code != 0:
    print(f"\n❌ ERROR: Step 1.2 failed with exit code {exit_code}")
    sys.exit(1)
print("✅ Step 1.2 completed successfully!\n")

# Step 1.3: Outlier Detection (Optional - creates visualizations)
print("\n[3/7] STEP 1.3: OUTLIER DETECTION & ANALYSIS")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_3_outlier_detection.py')}")
if exit_code != 0:
    print(f"\n⚠️  WARNING: Step 1.3 failed with exit code {exit_code}")
    print("Continuing with pipeline (outlier detection is optional)...\n")
else:
    print("✅ Step 1.3 completed successfully!\n")

# Step 1.3.1: Time-based features
print("\n[4/7] STEP 1.3.1: TIME-BASED FEATURES")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_3_1_time_features.py')}")
if exit_code != 0:
    print(f"\n❌ ERROR: Step 1.3.1 failed with exit code {exit_code}")
    sys.exit(1)
print("✅ Step 1.3.1 completed successfully!\n")

# Step 1.3.2: Lag features
print("\n[5/7] STEP 1.3.2: LAG & ROLLING FEATURES")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_3_2_lag_features.py')}")
if exit_code != 0:
    print(f"\n❌ ERROR: Step 1.3.2 failed with exit code {exit_code}")
    sys.exit(1)
print("✅ Step 1.3.2 completed successfully!\n")

# Step 1.3.3: Categorical encoding
print("\n[6/7] STEP 1.3.3: CATEGORICAL ENCODING")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_3_3_encode_categorical.py')}")
if exit_code != 0:
    print(f"\n❌ ERROR: Step 1.3.3 failed with exit code {exit_code}")
    sys.exit(1)
print("✅ Step 1.3.3 completed successfully!\n")

# Step 1.3.4: Normalization
print("\n[7/7] STEP 1.3.4: FEATURE NORMALIZATION (FINAL)")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_3_4_normalize_features_final.py')}")
if exit_code != 0:
    print(f"\n❌ ERROR: Step 1.3.4 failed with exit code {exit_code}")
    sys.exit(1)
print("✅ Step 1.3.4 completed successfully!\n")

# Step 1.4: EDA Analysis (Optional - creates visualizations)
print("\n[BONUS] STEP 1.4: EXPLORATORY DATA ANALYSIS (EDA)")
print("-" * 50)
exit_code = os.system(f"{sys.executable} {os.path.join(stage1_dir, 'step_1_4_eda_analysis.py')}")
if exit_code != 0:
    print(f"\n⚠️  WARNING: Step 1.4 failed with exit code {exit_code}")
    print("Continuing (EDA is optional for visualization purposes)...\n")
else:
    print("✅ Step 1.4 completed successfully!\n")

# Final summary
print("\n" + "="*70)
print("🎉 STAGE 1 PIPELINE COMPLETED SUCCESSFULLY! 🎉")
print("="*70)
print("\n📊 Final Outputs:")
print("\n1. Merged Data:")
print("   stage1/processed_data/Stage1.1/")
print("   ├─ train_merged.csv")
print("   └─ test_merged.csv")
print("\n2. Cleaned Data:")
print("   stage1/processed_data/Stage1.2/")
print("   ├─ train_cleaned_step2.csv")
print("   └─ test_cleaned_step2.csv")
print("\n3. Feature-Engineered Data:")
print("   stage1/processed_data/Stage1.3.4_Final/")
print("   ├─ train_final.csv (421,570 rows × 49 features)")
print("   ├─ test_final.csv (115,064 rows × 31 features)")
print("   └─ normalization_params.json")
print("\n4. Visualizations:")
print("   stage1/visualizations/")
print("   ├─ Stage1.3/ (4 outlier analysis plots)")
print("   └─ Stage1.4/ (10 EDA visualization plots)")
print("\n" + "="*70)
print("✅ Ready for Stage 2 (Advanced Analysis & Feature Engineering)!")
print("="*70)

