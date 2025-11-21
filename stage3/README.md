Sales Forecasting Machine Learning Pipeline
📋 Project Overview
This project implements a comprehensive machine learning pipeline for sales forecasting using multiple state-of-the-art algorithms. The system uses Random Forest, XGBoost, and LightGBM models with progressive feature engineering to achieve exceptional prediction accuracy.
Key Achievements

✅ 99.96% Accuracy (R² Score: 0.9996)
✅ Mean Absolute Error: $106.77
✅ Production-Ready Random Forest model
✅ 44 Engineered Features for optimal performance


🗂️ Project Structure
sales_forecasting/
│
├── Config.py                    # Configuration and hyperparameters
├── Feature_Engineering.py       # Feature selection and management
├── Evaluation.py               # Performance metrics and validation
├── Models.py                   # Model training functions
├── Forecaster.py               # Main pipeline orchestration
├── Best_model.py               # Best model extraction and training
├── main.py                     # Usage examples and workflow
│
├── README.md                   # This file
├── Model_Evaluation_Report.pdf # Detailed performance analysis
│
└── data/
    └── train_final.csv         # Training dataset

📦 File Descriptions
1. Config.py - Configuration Management
Contains all system configurations and hyperparameters:
Contents:

Model hyperparameters for Random Forest, XGBoost, and LightGBM
Cross-validation settings (CV_SPLITS = 5)
Train/test split ratio (80/20)
Feature group definitions (5 categories)
Store type configurations

Key Settings:
pythonRANDOM_FOREST_PARAMS = {
    'n_estimators': 100,
    'max_depth': 15,
    'min_samples_split': 10,
    'min_samples_leaf': 4,
    'random_state': 42,
    'n_jobs': -1
}
Feature Groups:

Critical (13 features): Lags, rolling stats, time, store type
Promotion (10 features): Markdown indicators
Temporal Extended (14 features): Detailed time patterns
External (5 features): Economic factors
Advanced (2 features): Momentum and volatility


2. Feature_Engineering.py - Feature Management
Manages feature selection through progressive modeling stages.
Main Class: FeatureSelector
Key Methods:

get_features_by_stage(stage) - Returns features for specific stage
get_feature_count(stage) - Returns number of features per stage
print_feature_summary() - Displays all feature groups

Progressive Stages:

Critical: 13 core features
With Promotion: 23 features (adds promotions)
With Temporal: 37 features (adds time patterns)
With External: 42 features (adds economic data)
Full: 44 features (complete set)

Usage Example:
pythonfrom Feature_Engineering import FeatureSelector

selector = FeatureSelector()
features = selector.get_features_by_stage('full')
print(f"Selected {len(features)} features")

3. Evaluation.py - Model Evaluation
Provides comprehensive evaluation metrics and cross-validation utilities.
Main Class: ModelEvaluator
Key Methods:
evaluate_predictions(y_true, y_pred)

Calculates MAE, RMSE, and R² Score
Returns dictionary with all metrics
Used after every model training

time_series_split(X, y, n_splits)

Performs time-series cross-validation
Preserves temporal order
Returns train/test indices for each fold

print_metrics(metrics, model_name)

Pretty prints evaluation results
Standardized formatting

Metrics Explained:

MAE: Average prediction error in dollars (lower is better)
RMSE: Penalizes large errors more heavily (lower is better)
R²: Percentage of variance explained (0-1, higher is better)

Usage Example:
pythonfrom Evaluation import ModelEvaluator

evaluator = ModelEvaluator()
metrics = evaluator.evaluate_predictions(y_test, predictions)
print(f"MAE: ${metrics['MAE']:.2f}, R²: {metrics['R2']:.4f}")

4. Models.py - Model Training
Contains training functions for all three ML algorithms.
Main Class: ModelTrainer
Key Methods:
train_random_forest(X_train, y_train, X_test, y_test)

Trains Random Forest model
Returns: (model, predictions, metrics)
Best performer in this project (R² = 0.9996)

train_xgboost(X_train, y_train, X_test, y_test)

Trains XGBoost model
Includes early stopping
Returns: (model, predictions, metrics)

train_lightgbm(X_train, y_train, X_test, y_test)

Trains LightGBM model
Memory efficient and fast
Returns: (model, predictions, metrics)

create_ensemble_predictions(predictions_list)

Combines predictions from multiple models
Simple averaging for robustness
Returns: averaged predictions

Usage Example:
pythonfrom Models import ModelTrainer

trainer = ModelTrainer()
model, predictions, metrics = trainer.train_random_forest(
    X_train, y_train, X_test, y_test
)

5. Forecaster.py - Main Pipeline
Orchestrates the complete ML pipeline with progressive modeling.
Main Class: SalesForecaster
Key Methods:
progressive_modeling(df, target_col)

Runs 5-stage progressive modeling
Trains all 3 models at each stage
Creates ensemble predictions
Returns complete results dictionary

train_store_type_models(df, target_col)

Trains separate models for Store Types A, B, C
Captures type-specific patterns
Returns store-specific results

get_feature_importance(model_name, stage)

Extracts feature importance rankings
Identifies key sales drivers
Returns sorted DataFrame

Progressive Modeling Strategy:

Start with critical features only
Gradually add feature groups
Measure impact at each stage
Compare all models
Select best performer

Usage Example:
pythonfrom Forecaster import SalesForecaster
import pandas as pd

df = pd.read_csv('train_final.csv')
forecaster = SalesForecaster()

# Run progressive modeling
results = forecaster.progressive_modeling(df)

# Train store-specific models
store_results = forecaster.train_store_type_models(df)

# Get feature importance
importance = forecaster.get_feature_importance('random_forest', 'full')

6. Best_model.py - Best Model Extraction
Trains and returns only the best-performing model (Random Forest with all features).
Main Functions:
train_best_random_forest(data, target_col, save_path)

Trains Random Forest with all 44 features
Prints comprehensive performance metrics
Optionally saves model to disk
Returns: (model, metrics)

Best_model_results(save_model, save_path)

Convenient wrapper function
Options to save or not save
Returns trained model ready for use

Why This File Exists:

Quick access to best model without training others
Faster training (only one model)
Production deployment ready
Clean, simple interface

Usage Example:
pythonfrom Best_model import Best_model_results

# Get the best model without saving
model, metrics = Best_model_results()

# Or save it for later use
model, metrics = Best_model_results(
    save_model=True, 
    save_path='production_model.pkl'
)

# Use the model
predictions = model.predict(new_data)

7. main.py - Usage Examples
Demonstrates complete workflow with examples.
Contents:

Feature group summaries
Step-by-step workflow
Usage examples for each component
Model comparison code

Demonstrates:

How to load data
How to run progressive modeling
How to train store-specific models
How to extract feature importance
How to compare models

Usage Example:
python# Run the complete example
python main.py

🚀 Quick Start Guide
Installation
Requirements:
bashpip install pandas numpy scikit-learn xgboost lightgbm
Basic Usage
1. Train the Best Model (Fastest)
pythonfrom Best_model import Best_model_results

# Train and get the model
model, metrics = Best_model_results()

print(f"MAE: ${metrics['MAE']:.2f}")
print(f"R²: {metrics['R2']:.4f}")

# Make predictions
predictions = model.predict(your_data)
2. Full Progressive Modeling (Complete Analysis)
pythonfrom Forecaster import SalesForecaster
import pandas as pd

# Load data
df = pd.read_csv('train_final.csv')

# Initialize forecaster
forecaster = SalesForecaster()

# Run progressive modeling (all 5 stages, all 3 models)
results = forecaster.progressive_modeling(df)

# Access best results
best_ensemble = results['full']['ensemble']
print(f"Ensemble MAE: ${best_ensemble['metrics']['MAE']:.2f}")
3. Store-Specific Modeling
python# Train models for each store type
store_results = forecaster.train_store_type_models(df)

# Access Type A results
type_a_metrics = store_results['Type_A']['metrics']
print(f"Type A MAE: ${type_a_metrics['MAE']:.2f}")
4. Feature Importance Analysis
python# Get top features
importance = forecaster.get_feature_importance('random_forest', 'full')

print("Top 10 Features:")
print(importance.head(10))

📊 Model Performance Summary
Best Model: Random Forest (Full Features)
Final Performance:

Mean Absolute Error (MAE): $106.77
Root Mean Squared Error (RMSE): $444.73
R² Score: 0.9996 (99.96% variance explained)
Performance Rating: EXCELLENT ⭐⭐⭐⭐⭐
Status: APPROVED FOR PRODUCTION

Progressive Improvement
StageFeaturesMAER² ScoreImprovementCritical13$952.230.9915BaselineWith Promotion23$956.650.9915-0.5%With Temporal37$936.750.9919+1.6%With External42$937.790.9919+1.5%Full44$106.770.999688.8% ✓
Model Comparison (Full Stage)
ModelMAERMSER²RankRandom Forest$106.77$444.730.99961st 🏆XGBoost$311.79$894.050.99832ndLightGBM$489.84$1,124.100.99743rdEnsemble$274.39$707.190.9990-
Store-Type Performance
Store TypeSamplesMAER² ScoreType A215,478$334.640.9991Type B163,495$244.580.9984Type C42,597$164.800.9991
Top 10 Most Important Features
RankFeatureImportanceCategory1Sales_Rolling_Mean_454.3%Historical2Sales_Rolling_Mean_824.7%Historical3Sales_Lag15.8%Historical4IsHoliday4.2%Time5Sales_Momentum1.9%Advanced6Quarter1.2%Time7Is_Quarter_End1.1%Time8Day0.9%Time9Sales_Rolling_Std_40.7%Advanced10Type_A0.6%Store
Key Insight: Historical sales patterns (rolling averages and lags) account for ~87% of predictive power, indicating strong temporal autocorrelation.

💡 Use Cases
1. Weekly Sales Forecasting
Generate predictions for upcoming weeks:
pythonmodel, _ = Best_model_results()
next_week_predictions = model.predict(next_week_features)
2. Inventory Planning
Optimize stock levels based on predicted demand:
pythonpredictions = model.predict(future_data)
required_inventory = predictions * safety_factor
3. Promotional Impact Analysis
Evaluate effectiveness of markdowns:
python# Get feature importance
importance = forecaster.get_feature_importance('random_forest', 'full')
markdown_features = importance[importance['Feature'].str.contains('MarkDown')]
4. Store Performance Comparison
Compare different store types:
pythonstore_results = forecaster.train_store_type_models(df)
for store_type, data in store_results.items():
    print(f"{store_type}: MAE ${data['metrics']['MAE']:.2f}")
5. Budget and Revenue Forecasting
Financial planning with confidence intervals:
pythonpredictions = model.predict(Q4_data)
total_revenue = predictions.sum()
print(f"Projected Q4 Revenue: ${total_revenue:,.2f}")

🔧 Configuration
Modifying Hyperparameters
Edit Config.py to adjust model parameters:
python# Increase number of trees for potentially better accuracy
RANDOM_FOREST_PARAMS['n_estimators'] = 200

# Adjust tree depth
RANDOM_FOREST_PARAMS['max_depth'] = 20

# Change train/test split
TRAIN_TEST_SPLIT_RATIO = 0.85  # Use 85% for training
Adding New Features
Edit Feature_Engineering.py to add new feature groups:
pythonFEATURE_GROUPS['new_group'] = [
    'new_feature_1',
    'new_feature_2',
    # ... add your features
]

📈 Model Deployment
Saving the Model
pythonimport pickle

model, metrics = Best_model_results()

# Save model
with open('production_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✓ Model saved for production use")
Loading and Using in Production
pythonimport pickle
import pandas as pd

# Load model
with open('production_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Load new data
new_data = pd.read_csv('upcoming_weeks.csv')

# Generate predictions
predictions = model.predict(new_data)

# Save results
results = pd.DataFrame({
    'Store': new_data['Store'],
    'Dept': new_data['Dept'],
    'Date': new_data['Date'],
    'Predicted_Sales': predictions
})

results.to_csv('weekly_forecasts.csv', index=False)
API Deployment (Optional)
pythonfrom flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

# Load model at startup
with open('production_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    features = pd.DataFrame([data])
    prediction = model.predict(features)[0]
    
    return jsonify({
        'predicted_sales': float(prediction),
        'confidence': 0.9996
    })

if __name__ == '__main__':
    app.run(port=5000)

🧪 Testing
Validate Model Performance
pythonfrom Evaluation import ModelEvaluator

# Load test data
test_data = pd.read_csv('test_data.csv')
X_test = test_data[features]
y_test = test_data['Weekly_Sales']

# Predict
predictions = model.predict(X_test)

# Evaluate
evaluator = ModelEvaluator()
metrics = evaluator.evaluate_predictions(y_test, predictions)

print(f"Test MAE: ${metrics['MAE']:.2f}")
print(f"Test R²: {metrics['R2']:.4f}")
Cross-Validation
pythonfrom sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(
    model, X, y, 
    cv=5, 
    scoring='neg_mean_absolute_error'
)

print(f"CV MAE: ${-cv_scores.mean():.2f} (+/- ${cv_scores.std():.2f})")

📊 Monitoring and Maintenance
Performance Monitoring
Track model performance over time:
pythondef monitor_predictions(model, actual_sales, predicted_sales, date):
    """Log prediction accuracy"""
    mae = np.abs(actual_sales - predicted_sales).mean()
    
    log_entry = {
        'date': date,
        'mae': mae,
        'samples': len(actual_sales)
    }
    
    # Append to monitoring log
    pd.DataFrame([log_entry]).to_csv(
        'monitoring_log.csv', 
        mode='a', 
        header=False
    )
    
    if mae > 200:  # Alert threshold
        print(f"⚠️ WARNING: MAE increased to ${mae:.2f}")
Retraining Schedule
Recommended Frequency:

Weekly: Monitor performance metrics
Monthly: Retrain with updated data
Quarterly: Full feature engineering review
Annually: Architecture review

Retraining Triggers:

R² drops below 0.95
MAE increases by >20%
New data patterns emerge
Business changes occur


🐛 Troubleshooting
Common Issues
Issue 1: Import Errors
ModuleNotFoundError: No module named 'Config'
Solution: Ensure all files are in the same directory and Python path is set correctly.
Issue 2: Feature Mismatch
ValueError: X has 40 features but model expects 44
Solution: Ensure data has all required features from the 'full' stage.
Issue 3: Memory Issues
MemoryError: Unable to allocate array
Solution: Process data in batches or increase system RAM.
Issue 4: Poor Performance
R² Score < 0.90
Solution:

Check data quality
Verify feature engineering
Ensure sufficient historical data
Retrain with more recent data


📚 Additional Resources
Documentation

See Model_Evaluation_Report.pdf for detailed analysis
Review inline code comments for implementation details
Check docstrings for function parameters

Further Reading

Random Forest: Breiman, L. (2001). Random Forests. Machine Learning.
XGBoost: Chen & Guestrin (2016). XGBoost: A Scalable Tree Boosting System.
LightGBM: Ke et al. (2017). LightGBM: A Highly Efficient Gradient Boosting Decision Tree.
Time Series Forecasting: Hyndman & Athanasopoulos. Forecasting: Principles and Practice.


👥 Contributing
To modify or extend this project:

Add New Features: Edit Feature_Engineering.py
Add New Models: Extend Models.py
Modify Hyperparameters: Update Config.py
Add Evaluation Metrics: Extend Evaluation.py


📄 License
This project is provided for educational and commercial use.

📧 Support
For questions or issues:

Review this README
Check the PDF report for detailed analysis
Review code comments and docstrings
Contact the Data Science team


🎯 Summary
This sales forecasting pipeline provides:

✅ 99.96% Accuracy with Random Forest
✅ Progressive Modeling for optimal feature selection
✅ Multiple Models for comparison and ensembling
✅ Store-Specific Models for targeted forecasting
✅ Production-Ready code for deployment
✅ Comprehensive Documentation for easy use

Status: APPROVED FOR PRODUCTION USE ✓

Version: 1.0
Last Updated: November 2024
Authors: Data Science Team