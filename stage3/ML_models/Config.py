# Configuration file containing all hyperparameters and model settings---------------------------------------------------

# Model hyperparameters for Random Forest
RANDOM_FOREST_PARAMS = {
    'n_estimators': 100,
    'max_depth': 15,
    'min_samples_split': 10,
    'min_samples_leaf': 4,
    'random_state': 42,
    'n_jobs': -1
}

# Model hyperparameters for XGBoost
XGBOOST_PARAMS = {
    'n_estimators': 100,
    'max_depth': 8,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42,
    'n_jobs': -1
}

# Model hyperparameters for LightGBM
LIGHTGBM_PARAMS = {
    'n_estimators': 100,
    'max_depth': 8,
    'learning_rate': 0.1,
    'num_leaves': 31,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'random_state': 42,
    'n_jobs': -1,
    'verbose': -1
}

# Cross-validation settings
CV_SPLITS = 5
TRAIN_TEST_SPLIT_RATIO = 0.8

# Feature groups for progressive modeling
FEATURE_GROUPS = {
    'critical': [
        'Sales_Lag1', 'Sales_Lag2', 'Sales_Lag4',
        'Sales_Rolling_Mean_4', 'Sales_Rolling_Mean_8',
        'Month', 'Quarter',
        'Month_Sin', 'Month_Cos',
        'IsHoliday',
        'Type_A', 'Type_B', 'Type_C'
    ],
    'promotion': [
        'Has_MarkDown1', 'Has_MarkDown2', 'Has_MarkDown3',
        'Has_MarkDown4', 'Has_MarkDown5',
        'MarkDown1', 'MarkDown2', 'MarkDown3', 'MarkDown4', 'MarkDown5'
    ],
    'temporal_extended': [
        'Day', 'DayOfWeek', 'WeekOfYear',
        'Week_Sin', 'Week_Cos', 'DayOfWeek_Sin', 'DayOfWeek_Cos',
        'Is_Weekend', 'Is_Month_Start', 'Is_Month_End',
        'Is_Quarter_Start', 'Is_Quarter_End', 'Is_Year_Start', 'Is_Year_End'
    ],
    'external': [
        'Temperature', 'Fuel_Price', 'CPI', 'Unemployment', 'Size'
    ],
    'advanced': [
        'Sales_Rolling_Std_4', 'Sales_Momentum'
    ]
}

# Progressive modeling stages
MODELING_STAGES = ['critical', 'with_promotion', 'with_temporal', 'with_external', 'full']

# Store types
STORE_TYPES = ['Type_A', 'Type_B', 'Type_C']