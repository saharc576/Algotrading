from asyncio import threads
import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
import yfinance as yf
from yahoo_fin.stock_info import get_data
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns; 
sns.set(style="whitegrid")

def stationarity_test(X, cutoff=0.01):
    # H_0 in adfuller is unit root exists (non-stationary)
    # We must observe significant p-value to convince ourselves that the series is stationary
    pvalue = adfuller(X)[1]
    if pvalue < cutoff:
        print('p-value = ' + str(pvalue) + ' The series ' + X.name +' is likely stationary.')
    else:
        print('p-value = ' + str(pvalue) + ' The series ' + X.name +' is likely non-stationary.')


def is_cointegrated_pair(x, y):
    """:returns True iff pvalue is small enough (=lower than threshold)"""
    threshold = 0.05
    score, pvalue, _ = coint(x,y)
    print(pvalue)
    return pvalue < threshold

def zscore(series):
    """Calculate z-score. normalize the series, since the absolute ratio isn't very useful in statistical terms
        ZScore (Value) = (Value — Mean) / Standard Deviation
    """
    return (series - series.mean()) / np.std(series)