# Main entry point for the sales forecasting pipeline.
# Usage examples and workflow demonstration.
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from Forecaster import SalesForecaster
from Feature_Engineering import FeatureSelector
from Best_model import train_best_random_forest, data
from pathlib import Path

# Get correct path to training data
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_PATH = PROJECT_ROOT / 'stage1' / 'processed_data' / 'Stage1.3.4_Final' / 'train_final.csv'
df = pd.read_csv(DATA_PATH)

# Main function demonstrating usage of the SalesForecaster class.
def main():

    print("="*60)
    print("SALES FORECASTING ML PIPELINE")
    print("="*60)
    
    # Initialize forecaster
    forecaster = SalesForecaster()
    
    # Print feature information
    forecaster.feature_selector.print_feature_summary()
    
    print("\n" + "="*60)
    print("WORKFLOW:")
    print("="*60)

if __name__ == "__main__":
    main()

forecaster = SalesForecaster()


# comparing all features groups applyed on all models to find the best model-----------------------------
# Best model after running (random_forest) in the feature stage (full) >>> all features used
# + feature importance to know which features drive predictions most and which features might be redundant 
def All_models_results():
   
   results = forecaster.progressive_modeling(df, target_col='Weekly_Sales')
   importance = forecaster.get_feature_importance('random_forest', 'full')
   print("\\nTop 10 Most Important Features:")
   print(importance.head(10))
   return results

# Advanced models for each store type -------------------------------------------------------------------
def Store_type_models():
   
   store_results = forecaster.train_store_type_models(df)
   return store_results


# to access the best model directly----------------------------------------------------------------------
def Best_model_results():
    results = train_best_random_forest(data,'Weekly_Sales', None)
    return results


# to run >>> All_models_results()
# to run >>> Store_type_models()
# to run >>> Best_model_results()
# End of ML_models/main.py ------------------------------------------------------------------------------
