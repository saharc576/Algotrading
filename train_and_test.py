import numpy as np  # to handle matrix
import pandas as pd # to handle data
from matplotlib import pyplot as plt # to visualize
import datetime, pytz # to handle time
from sklearn.model_selection import train_test_split # Split data
from sklearn.ensemble import RandomForestRegressor # Random Forest Classifier

"""Python file to load csv file, split it and train it
    Then, store the model.
"""

def read_and_parse_csv_file(file_name: str):
    df = pd.read_csv(file_name, parse_dates=[0], date_parser=dateparse)
    # First thing is to fix the data for bars/candles where there are no trades. 
    # Volume/trades are a single event so fill "NaN"s with zeroes for relevant fields...
    df['Volume_(BTC)'].fillna(value=0, inplace=True)
    df['Volume_(Currency)'].fillna(value=0, inplace=True)
    df['Weighted_Price'].fillna(value=0, inplace=True)

    # Secondly, we need to fix the OHLC (open, high, low, close) data which is a continuous timeseries so
    # let's fill forwards those values.
    df['Open'].fillna(method='ffill', inplace=True)
    df['High'].fillna(method='ffill', inplace=True)
    df['Low'].fillna(method='ffill', inplace=True)
    df['Close'].fillna(method='ffill', inplace=True)
    df.tail(3)

def dateparse (time_in_secs):    
    return pytz.utc.localize(datetime.datetime.fromtimestamp(float(time_in_secs)))

def split_data_to_train_and_test(data):
    prediction_days = 140
    df_train = historical_df[:len(historical_df) - prediction_days ]
    df_test  = historical_df[ len(historical_df) - prediction_days:]

    print("PERCENT test/total data = %", (prediction_days/len(historical_df)) * 100)
    print("train data shape:", df_train.shape)
    print("test data shape:", df_test.shape)

    training_set = df_train.values
    X_train = training_set[0:len(training_set), 0:49]
    y_train = training_set[0:len(training_set), 49].reshape(-1,1)

    test_set = df_test.values
    X_test = test_set[0:len(test_set), 0:49]
    y_test = test_set[0:len(test_set), 49].reshape(-1,1)

    df_train.head(3)


