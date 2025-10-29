import os
import sys

# Task 2.1: Advanced Data Analysis
exit_code = os.system(f"{sys.executable} stage2/step_2_1_advanced_analysis.py")
if exit_code != 0:
    print(f"\nERROR: Step 2.1 failed with exit code {exit_code}")
    sys.exit(1)

# Task 2.2: Enhanced Feature Engineering
exit_code = os.system(f"{sys.executable} stage2/step_2_2_feature_engineering.py")
if exit_code != 0:
    print(f"\nERROR: Step 2.2 failed with exit code {exit_code}")
    sys.exit(1)

# Task 2.3: Advanced Visualizations
exit_code = os.system(f"{sys.executable} stage2/step_2_3_advanced_visualizations.py")
if exit_code != 0:
    print(f"\nERROR: Step 2.3 failed with exit code {exit_code}")
    sys.exit(1)

