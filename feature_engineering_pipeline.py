"""
Feature Engineering Pipeline - Steps 1.3.1 through 1.3.4
=========================================================
This script runs all feature engineering steps sequentially.

Pipeline Flow:
  Stage1.2 → [Step 1.3.1] → Stage1.3.1 → [Step 1.3.2] → Stage1.3.2 
  → [Step 1.3.3] → Stage1.3.3 → [Step 1.3.4] → Stage1.3.4_Final

Input:  processed_data/Stage1.2/train_cleaned_step2.csv & test_cleaned_step2.csv
Output: processed_data/Stage1.3.4_Final/train_final.csv & test_final.csv
"""

import os
import sys

print("="*80)
print("FEATURE ENGINEERING PIPELINE")
print("="*80)
print("\nPipeline Flow:")
print("  Stage1.2 → [1.3.1] → Stage1.3.1 → [1.3.2] → Stage1.3.2")
print("  → [1.3.3] → Stage1.3.3 → [1.3.4] → Stage1.3.4_Final\n")

# Step 1: Time-based features
print("="*80)
print("[1/4] STEP 1.3.1: TIME-BASED FEATURES")
print("="*80)
print("Input:  processed_data/Stage1.2/")
print("Output: processed_data/Stage1.3.1/")
print("-"*80)
exit_code = os.system(f"{sys.executable} step_1_3_1_time_features.py")
if exit_code != 0:
    print(f"\n✗ ERROR: Step 1.3.1 failed with exit code {exit_code}")
    sys.exit(1)
print("-"*80)
print("✓ Output: processed_data/Stage1.3.1/train_time_features.csv")
print("✓ Output: processed_data/Stage1.3.1/test_time_features.csv")

# Step 2: Lag features
print("\n" + "="*80)
print("[2/4] STEP 1.3.2: LAG FEATURES")
print("="*80)
print("Input:  processed_data/Stage1.3.1/")
print("Output: processed_data/Stage1.3.2/")
print("-"*80)
exit_code = os.system(f"{sys.executable} step_1_3_2_lag_features.py")
if exit_code != 0:
    print(f"\n✗ ERROR: Step 1.3.2 failed with exit code {exit_code}")
    sys.exit(1)
print("-"*80)
print("✓ Output: processed_data/Stage1.3.2/train_lag_features.csv")
print("✓ Output: processed_data/Stage1.3.2/test_lag_features.csv")

# Step 3: Categorical encoding
print("\n" + "="*80)
print("[3/4] STEP 1.3.3: CATEGORICAL ENCODING")
print("="*80)
print("Input:  processed_data/Stage1.3.2/")
print("Output: processed_data/Stage1.3.3/")
print("-"*80)
exit_code = os.system(f"{sys.executable} step_1_3_3_encode_categorical.py")
if exit_code != 0:
    print(f"\n✗ ERROR: Step 1.3.3 failed with exit code {exit_code}")
    sys.exit(1)
print("-"*80)
print("✓ Output: processed_data/Stage1.3.3/train_encoded.csv")
print("✓ Output: processed_data/Stage1.3.3/test_encoded.csv")

# Step 4: Normalization
print("\n" + "="*80)
print("[4/4] STEP 1.3.4: FEATURE NORMALIZATION")
print("="*80)
print("Input:  processed_data/Stage1.3.3/")
print("Output: processed_data/Stage1.3.4_Final/")
print("-"*80)
exit_code = os.system(f"{sys.executable} step_1_3_4_normalize_features_final.py")
if exit_code != 0:
    print(f"\n✗ ERROR: Step 1.3.4 failed with exit code {exit_code}")
    sys.exit(1)
print("-"*80)
print("✓ Output: processed_data/Stage1.3.4_Final/train_final.csv")
print("✓ Output: processed_data/Stage1.3.4_Final/test_final.csv")
print("✓ Output: processed_data/Stage1.3.4_Final/normalization_params.json")

# Final summary
print("\n" + "="*80)
print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
print("="*80)
print("\nFinal Datasets Ready:")
print("  📁 processed_data/Stage1.3.4_Final/")
print("     ├─ train_final.csv")
print("     ├─ test_final.csv")
print("     └─ normalization_params.json")
print("\n🚀 Ready for Model Development!")
print("="*80)
