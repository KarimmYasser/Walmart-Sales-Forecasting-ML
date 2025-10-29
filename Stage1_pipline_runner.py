import os
import sys

print("="*80)
print("FEATURE ENGINEERING PIPELINE")
print("="*80)
print("\nPipeline Flow:")
print("  Stage1.2 → [1.3.1] → Stage1.3.1 → [1.3.2] → Stage1.3.2")
print("  → [1.3.3] → Stage1.3.3 → [1.3.4] → Stage1.3.4_Final\n")

# Step 1: Time-based features
exit_code = os.system(f"{sys.executable} step_1_3_1_time_features.py")
if exit_code != 0:
    print(f"\nERROR: Step 1.3.1 failed with exit code {exit_code}")
    sys.exit(1)

# Step 2: Lag features
exit_code = os.system(f"{sys.executable} step_1_3_2_lag_features.py")
if exit_code != 0:
    print(f"\nERROR: Step 1.3.2 failed with exit code {exit_code}")
    sys.exit(1)

# Step 3: Categorical encoding
exit_code = os.system(f"{sys.executable} step_1_3_3_encode_categorical.py")
if exit_code != 0:
    print(f"\nERROR: Step 1.3.3 failed with exit code {exit_code}")
    sys.exit(1)

# Step 4: Normalization
exit_code = os.system(f"{sys.executable} step_1_3_4_normalize_features_final.py")
if exit_code != 0:
    print(f"\nERROR: Step 1.3.4 failed with exit code {exit_code}")
    sys.exit(1)

