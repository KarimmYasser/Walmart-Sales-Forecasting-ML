"""
Quick test to verify predictions change with different inputs
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from deployment.predictor import SalesPredictor

predictor = SalesPredictor()

# Same store/dept but different dates
test_cases = [
    {"Store": 2, "Dept": 1, "Date": "2012-02-03", "Type": "A", "Size": 150000, "IsHoliday": False, "Temperature": 54.0, "Fuel_Price": 3.51, "CPI": 211.0, "Unemployment": 7.5},
    {"Store": 2, "Dept": 1, "Date": "2012-05-04", "Type": "A", "Size": 150000, "IsHoliday": False, "Temperature": 54.0, "Fuel_Price": 3.51, "CPI": 211.0, "Unemployment": 7.5},
    {"Store": 2, "Dept": 1, "Date": "2012-08-10", "Type": "A", "Size": 150000, "IsHoliday": False, "Temperature": 54.0, "Fuel_Price": 3.51, "CPI": 211.0, "Unemployment": 7.5},
    {"Store": 2, "Dept": 1, "Date": "2012-11-23", "Type": "A", "Size": 150000, "IsHoliday": True, "Temperature": 54.0, "Fuel_Price": 3.51, "CPI": 211.0, "Unemployment": 7.5},
]

print("Testing Store 2, Dept 1 with different dates:\n")
for i, test in enumerate(test_cases, 1):
    result = predictor.predict_single(test)
    print(f"{i}. Date: {test['Date']}, Holiday: {test['IsHoliday']:5} → ${result['predicted_sales']:,.2f}")

# Different stores same date
print("\n\nTesting different stores on same date (2012-11-23):\n")
stores_test = [
    {"Store": 1, "Dept": 1, "Date": "2012-11-23", "Type": "C", "Size": 151315, "IsHoliday": True, "Temperature": 54.0, "Fuel_Price": 3.51, "CPI": 211.0, "Unemployment": 7.5},
    {"Store": 4, "Dept": 1, "Date": "2012-11-23", "Type": "A", "Size": 202307, "IsHoliday": True, "Temperature": 54.0, "Fuel_Price": 3.51, "CPI": 211.0, "Unemployment": 7.5},
    {"Store": 10, "Dept": 1, "Date": "2012-11-23", "Type": "B", "Size": 126512, "IsHoliday": True, "Temperature": 54.0, "Fuel_Price": 3.51, "CPI": 211.0, "Unemployment": 7.5},
]

for test in stores_test:
    result = predictor.predict_single(test)
    print(f"Store {test['Store']:2}, Type {test['Type']}, Size {test['Size']:6} → ${result['predicted_sales']:,.2f}")
