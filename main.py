import pandas as pd

# Load datasets
train = pd.read_csv('datasets\walmart-recruiting-store-sales-forecasting\train.csv')
stores = pd.read_csv('datasets\walmart-recruiting-store-sales-forecasting\stores.csv')
features = pd.read_excel('datasets\walmart-recruiting-store-sales-forecasting\features.xlsx')   
test = pd.read_csv('datasets\walmart-recruiting-store-sales-forecasting\test.csv')

# Merge train with stores and features
train_full = train.merge(stores, on='Store', how='left')
train_full = train_full.merge(features, on=['Store', 'Date', 'IsHoliday'], how='left')