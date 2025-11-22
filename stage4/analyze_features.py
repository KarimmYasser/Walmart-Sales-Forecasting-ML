"""
Analyze which features have the most impact on predictions
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from deployment.predictor import SalesPredictor
import pandas as pd
import numpy as np

predictor = SalesPredictor()

# Get feature importances from the Random Forest model
feature_importances = predictor.model.feature_importances_
feature_names = predictor.features

# Create DataFrame and sort by importance
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importances
}).sort_values('Importance', ascending=False)

print("="*70)
print("TOP 20 MOST IMPORTANT FEATURES FOR PREDICTIONS")
print("="*70)
print("\nRank | Feature                      | Importance | Impact")
print("-" * 70)

for idx, row in importance_df.head(20).iterrows():
    feature = row['Feature']
    importance = row['Importance']
    percentage = importance * 100
    
    # Categorize the feature
    if 'Lag' in feature or 'Rolling' in feature or 'Momentum' in feature:
        category = "📊 Historical Sales"
    elif 'Month' in feature or 'Week' in feature or 'Day' in feature or 'Quarter' in feature or 'Year' in feature or 'Is_' in feature:
        category = "📅 Time/Season"
    elif 'Size' in feature or 'Type' in feature:
        category = "🏪 Store Characteristics"
    elif 'Dept' in feature:
        category = "🏷️  Department"
    elif 'Holiday' in feature:
        category = "🎉 Holiday"
    elif 'MarkDown' in feature:
        category = "💰 Promotions"
    else:
        category = "🌡️  External Factors"
    
    bar = "█" * int(percentage * 2)
    print(f"{idx+1:4} | {feature:28} | {percentage:5.2f}%   | {bar} {category}")

print("\n" + "="*70)
print("SUMMARY BY CATEGORY")
print("="*70)

categories = {
    'Historical Sales (Lag/Rolling)': 0,
    'Time/Season Features': 0,
    'Store Characteristics': 0,
    'Department': 0,
    'Holiday': 0,
    'Promotions': 0,
    'External Factors': 0
}

for idx, row in importance_df.iterrows():
    feature = row['Feature']
    importance = row['Importance']
    
    if 'Lag' in feature or 'Rolling' in feature or 'Momentum' in feature:
        categories['Historical Sales (Lag/Rolling)'] += importance
    elif 'Month' in feature or 'Week' in feature or 'Day' in feature or 'Quarter' in feature or 'Year' in feature or 'Is_' in feature:
        categories['Time/Season Features'] += importance
    elif 'Size' in feature or 'Type' in feature:
        categories['Store Characteristics'] += importance
    elif 'Dept' in feature:
        categories['Department'] += importance
    elif 'Holiday' in feature:
        categories['Holiday'] += importance
    elif 'MarkDown' in feature:
        categories['Promotions'] += importance
    else:
        categories['External Factors'] += importance

print("\nCategory                         | Total Importance | Contribution")
print("-" * 70)
for category, importance in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    percentage = importance * 100
    bar = "█" * int(percentage)
    print(f"{category:32} | {percentage:6.2f}%          | {bar}")

print("\n" + "="*70)
print("KEY INSIGHTS")
print("="*70)
print("\n🎯 To see the MOST variation in predictions, change these inputs:\n")

top_5 = importance_df.head(5)
for idx, row in top_5.iterrows():
    print(f"   {idx+1}. {row['Feature']:28} ({row['Importance']*100:.2f}% importance)")

print("\n💡 These features matter most because:")
print("   - Historical sales patterns (lag features) show past performance")
print("   - Time/seasonal features capture trends and cycles")
print("   - Store size and type affect overall sales capacity")
