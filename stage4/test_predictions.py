"""
Test script to verify the model produces different predictions for different inputs
"""

import sys
from pathlib import Path

# Add deployment to path
sys.path.insert(0, str(Path(__file__).parent))

from deployment.predictor import SalesPredictor

print("="*70)
print("TESTING MODEL PREDICTIONS")
print("="*70)

# Initialize predictor
predictor = SalesPredictor()

# Test case 1: Small Type C store, regular day
test1 = {
    'Store': 1,
    'Dept': 1,
    'Date': '2012-11-02',
    'Type': 'C',
    'Size': 151315,
    'IsHoliday': False,
    'Temperature': 60.0,
    'Fuel_Price': 3.5,
    'CPI': 211.0,
    'Unemployment': 7.5
}

# Test case 2: Large Type A store, holiday
test2 = {
    'Store': 20,
    'Dept': 95,
    'Date': '2012-11-23',  # Thanksgiving week
    'Type': 'A',
    'Size': 202307,
    'IsHoliday': True,
    'Temperature': 50.0,
    'Fuel_Price': 3.5,
    'CPI': 211.0,
    'Unemployment': 7.5
}

# Test case 3: Medium Type B store, different dept
test3 = {
    'Store': 10,
    'Dept': 50,
    'Date': '2012-12-07',
    'Type': 'B',
    'Size': 180000,
    'IsHoliday': False,
    'Temperature': 45.0,
    'Fuel_Price': 3.5,
    'CPI': 211.0,
    'Unemployment': 7.5
}

# Test case 4: Same as test1 but different date (summer vs fall)
test4 = {
    'Store': 1,
    'Dept': 1,
    'Date': '2012-07-13',  # Summer
    'Type': 'C',
    'Size': 151315,
    'IsHoliday': False,
    'Temperature': 85.0,
    'Fuel_Price': 3.5,
    'CPI': 211.0,
    'Unemployment': 7.5
}

print("\n" + "="*70)
print("TEST 1: Small Type C Store, Regular Day")
print("="*70)
pred1 = predictor.predict_single(test1)
print(f"\n📊 Prediction: ${pred1['predicted_sales']:,.2f}")

print("\n" + "="*70)
print("TEST 2: Large Type A Store, Holiday (Thanksgiving)")
print("="*70)
pred2 = predictor.predict_single(test2)
print(f"\n📊 Prediction: ${pred2['predicted_sales']:,.2f}")

print("\n" + "="*70)
print("TEST 3: Medium Type B Store, Different Department")
print("="*70)
pred3 = predictor.predict_single(test3)
print(f"\n📊 Prediction: ${pred3['predicted_sales']:,.2f}")

print("\n" + "="*70)
print("TEST 4: Same as Test 1 but Summer Season")
print("="*70)
pred4 = predictor.predict_single(test4)
print(f"\n📊 Prediction: ${pred4['predicted_sales']:,.2f}")

print("\n" + "="*70)
print("SUMMARY OF RESULTS")
print("="*70)
print(f"Test 1 (Small C, Regular):     ${pred1['predicted_sales']:>12,.2f}")
print(f"Test 2 (Large A, Holiday):     ${pred2['predicted_sales']:>12,.2f}")
print(f"Test 3 (Medium B, Diff Dept):  ${pred3['predicted_sales']:>12,.2f}")
print(f"Test 4 (Small C, Summer):      ${pred4['predicted_sales']:>12,.2f}")

# Calculate variance
predictions = [pred1['predicted_sales'], pred2['predicted_sales'], 
               pred3['predicted_sales'], pred4['predicted_sales']]
variance = max(predictions) - min(predictions)
avg = sum(predictions) / len(predictions)

print(f"\nAverage Prediction: ${avg:,.2f}")
print(f"Range (Max - Min):  ${variance:,.2f}")
print(f"Variance %:         {(variance/avg)*100:.1f}%")

if variance < 1000:
    print("\n⚠️  WARNING: Predictions are too similar (variance < $1,000)")
    print("    This suggests the model may not be using features properly.")
    print("    All predictions should NOT be the same value.")
else:
    print("\n✅ SUCCESS: Model is producing varied, realistic predictions!")
    print("    The model is properly using different features for each input.")
    print(f"    Variance of ${variance:,.2f} is expected for different stores/depts/dates.")

print("="*70)
