import numpy as np
import pandas as pd
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
import yfinance as yf
from yahoo_fin.stock_info import get_data
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")


def get_historical_Data(tickers):
    """This function returns a pd dataframe with all of the adjusted closing information"""
    data = pd.DataFrame()
    names = list()
    for i in tickers:
        data = pd.concat([data, pd.DataFrame(yf.download(i, start=datetime(2020, 10, 27), end=datetime(2021, 10, 27)).iloc[:,4])], axis = 1)
        names.append(i)
    data.columns = names
    return data

def use_tick(ticks):
    d = get_historical_Data(ticks)
    print(d.shape)
    # Most Recent Data
    #print(d.tail())
    return d

def corr_matrix(d):
    return d.corr()

def make_heat_map(corr_matrix):
    plt.figure(figsize=(8, 6), dpi=200)
    sns.heatmap(corr_matrix, annot=True)
    plt.show()

def BRK_B_compare_MSFT(d):
    BRK_B = d['BRK-B']
    MSFT = d['MSFT']
    plt.figure(figsize=(8, 6), dpi=200)
    plt.plot(BRK_B - MSFT, label='Spread (BRK-B - MSFT)')
    plt.legend()
    plt.title("Spread between NIKE and AAPL")

def Ratio(d , First, Second):
    # Also, we can take a look at the price ratios between the two time series.
    X = d[First]
    Y = d[Second]
    plt.figure(figsize=(8, 6), dpi=200)
    ratio = X / Y
    plt.plot(ratio, label=f'Price Ratio {First}/{Second})')
    plt.axhline(ratio.mean(), color='red')
    plt.legend()
    plt.title(f"Price Ratio between {First} and {Second}")
    plt.show()
    return ratio;

def graph_with_lines(ratio):
    plt.figure(figsize=(8, 6), dpi=200)
    # Calculate the Zscores of each row.
    df_zscore = (ratio - ratio.mean()) / ratio.std()
    plt.plot(df_zscore, label="Z Scores")
    plt.axhline(df_zscore.mean(), color='black')
    plt.axhline(1.0,
                color='red')  # Setting the upper and lower bounds to be the z score of 1 and -1 (1/-1 standard deviation)
    plt.axhline(1.25, color='red')  # 95% of our data will lie between these bounds.
    plt.axhline(-1.0, color='green')  # 68% of our data will lie between these bounds.
    plt.axhline(-1.25, color='green')  # 95% of our data will lie between these bounds.
    plt.legend(loc='best')
    plt.title('Z score of Ratio of Berkshire to MSFT')
    plt.show()
    # For the most part, the range that exists outside of these 'bands' must come converge back to the mean. Thus, you can
    # determine when you can go long or short the pair (BRK_B to MSFT).

def stationarity_test(X, cutoff=0.01):
    # H_0 in adfuller is unit root exists (non-stationary)
    # We must observe significant p-value to convince ourselves that the series is stationary
    pvalue = adfuller(X)[1]
    if pvalue < cutoff:
        print('p-value = ' + str(pvalue) + ' The series ' + X.name +' is likely stationary.')
    else:
        print('p-value = ' + str(pvalue) + ' The series ' + X.name +' is likely non-stationary.')



def find_cointegrated_pairs(data):
    n = data.shape[1]
    score_matrix = np.zeros((n, n))
    pvalue_matrix = np.ones((n, n))
    keys = data.keys()
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            S1 = data[keys[i]]
            S2 = data[keys[j]]
            result = coint(S1, S2)
            score = result[0]
            pvalue = result[1]
            score_matrix[i, j] = score
            pvalue_matrix[i, j] = pvalue
            if pvalue < 0.05:
                pairs.append((keys[i], keys[j]))
    return score_matrix, pvalue_matrix, pairs



def trade(S1, S2, window1, window2):
    
    # If window length is 0, algorithm doesn't make sense, so exit
    if (window1 == 0) or (window2 == 0):
        return 0

    # Compute rolling mean and rolling standard deviation
    ratios = S1/S2
    ma1 = ratios.rolling(window=window1,
                               center=False).mean()
    ma2 = ratios.rolling(window=window2,
                               center=False).mean()
    std = ratios.rolling(window=window2,
                        center=False).std()
    zscore = (ma1 - ma2)/std
    
    # Simulate trading
    # Start with no money and no positions
    money = 0
    countS1 = 0
    countS2 = 0
    for i in range(len(ratios)):
        # Sell short if the z-score is > 1
        if zscore[i] < -1:
            money += S1[i] - S2[i] * ratios[i]
            countS1 -= 1
            countS2 += ratios[i]
            #print('Selling Ratio %s %s %s %s'%(money, ratios[i], countS1,countS2))
        # Buy long if the z-score is < -1
        elif zscore[i] > 1:
            money -= S1[i] - S2[i] * ratios[i]
            countS1 += 1
            countS2 -= ratios[i]
            #print('Buying Ratio %s %s %s %s'%(money,ratios[i], countS1,countS2))
        # Clear positions if the z-score between -.5 and .5
        elif abs(zscore[i]) < 0.75:
            money += S1[i] * countS1 + S2[i] * countS2
            countS1 = 0
            countS2 = 0
            #print('Exit pos %s %s %s %s'%(money,ratios[i], countS1,countS2))
            
            
    return money



if __name__ == "__main__":

    ticks = ["BTC-USD", "AAPL", "GOOG", "AMD", "GME", "SPY", "NFLX", "BA", "WMT","TWTR","GS","XOM","NKE","FEYE", "FB","BRK-B", "MSFT"] #Name of company (Dominos pizza)
    d = use_tick(ticks)
    x,y,pairs=find_cointegrated_pairs(d)
    print(pairs)
    # r = Ratio(d, "BTC-USD", "ETH-USD")
    # graph_with_lines(r)