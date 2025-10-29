"""
Stage 2 Pipeline - Advanced Analysis and Feature Engineering
=============================================================
This script runs all Stage 2 tasks sequentially:
1. Advanced Data Analysis (time series, correlation, stationarity)
2. Enhanced Feature Engineering (42 additional features)
3. Advanced Visualizations (10 professional plots)

Can be run from either the project root or the stage2/ directory.

Input:  ../stage1/processed_data/Stage1.3.4_Final/train_final.csv & test_final.csv
Output: outputs/ (analysis_results, enhanced_features, visualizations)
"""

import os
import sys

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)  # Change to script directory to ensure correct paths

print("="*80)
print("STAGE 2 PIPELINE - ADVANCED ANALYSIS & FEATURE ENGINEERING")
print("="*80)
print("\nPipeline Flow:")
print("  Stage1.3.4_Final -> [2.1] -> Analysis -> [2.2] -> Enhanced Features")
print("  -> [2.3] -> Advanced Visualizations\n")

# Task 2.1: Advanced Data Analysis
print("="*80)
print("[1/3] TASK 2.1: ADVANCED DATA ANALYSIS")
print("="*80)
print("Input:  ../stage1/processed_data/Stage1.3.4_Final/train_final.csv")
print("Output: outputs/analysis_results/ & visualizations/")
print("-"*80)
exit_code = os.system(f"{sys.executable} step_2_1_advanced_analysis.py")
if exit_code != 0:
    print(f"\nERROR: Step 2.1 failed with exit code {exit_code}")
    sys.exit(1)
print("-"*80)
print("Output: ADF test, correlation matrix, holiday stats")
print("Visualizations: time series decomposition, correlation heatmap, holiday impact\n")

# Task 2.2: Enhanced Feature Engineering
print("="*80)
print("[2/3] TASK 2.2: ENHANCED FEATURE ENGINEERING")
print("="*80)
print("Input:  ../stage1/processed_data/Stage1.3.4_Final/")
print("Output: outputs/enhanced_features/")
print("-"*80)
exit_code = os.system(f"{sys.executable} step_2_2_feature_engineering.py")
if exit_code != 0:
    print(f"\nERROR: Step 2.2 failed with exit code {exit_code}")
    sys.exit(1)
print("-"*80)
print("Output: train_enhanced.csv (91 features)")
print("Output: test_enhanced.csv (73 features)")
print("Output: feature_summary.json\n")

# Task 2.3: Advanced Visualizations
print("="*80)
print("[3/3] TASK 2.3: ADVANCED VISUALIZATIONS")
print("="*80)
print("Input:  outputs/enhanced_features/train_enhanced.csv")
print("Output: outputs/visualizations/")
print("-"*80)
exit_code = os.system(f"{sys.executable} step_2_3_advanced_visualizations.py")
if exit_code != 0:
    print(f"\nERROR: Step 2.3 failed with exit code {exit_code}")
    sys.exit(1)
print("-"*80)
print("Output: 10 advanced visualizations created\n")

# Final summary
print("="*80)
print("STAGE 2 PIPELINE COMPLETED SUCCESSFULLY!")
print("="*80)
print("\nAnalysis Outputs:")
print("  outputs/")
print("     |- analysis_results/")
print("     |  |- adf_test_results.json")
print("     |  |- correlation_matrix.csv")
print("     |  |- sales_correlations.csv")
print("     |  `- holiday_impact_stats.csv")
print("     |- enhanced_features/")
print("     |  |- train_enhanced.csv (421,570 x 91)")
print("     |  |- test_enhanced.csv (115,064 x 73)")
print("     |  `- feature_summary.json")
print("     `- visualizations/")
print("        `- [13 professional visualizations]")
print("\nReady for Milestone 3 (Model Development)!")
print("="*80)

