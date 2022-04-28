# Pairs Trading

## Basic Idea
    1) Find 2 assets that move similarly with eachother (whether it be a negative or positive correlation)
    2) Sell the 'overvalued' stock and buy the 'undervalued' stock -- A common signal to use to triger the purchase of a pair trade is to use the Price Ratio (Stock A / Stock B). If the ratio changes significantly, then you know it is time to trade. 'Significance' can be measured with standard deviation.

## Step 1 - Indicator
    Here we are trying to create a signal that tells us if the ratio is a buy or a sell at the next instant in time, i.e our prediction variable Y:
    Y = Ratio is buy (1) or sell (-1)
    Y(t)= Sign( Ratio(t+1) — Ratio(t) )
    Note we don’t need to predict actual stock prices, or even actual value of ratio (though we could), just the direction of next move in ratio


## Step 2 - Collect data
    Pull data from Yahoo finance (or any other reliable source).
    We are using the following data: daily intervals for trading days over last 10 years (~2500 data points): Open, Close, High, Low and Trading Volume

## Step 3 - Split data (train and test)
    Split the data 80% - 20%
    Train using Random Forest. 
    Test model.

## Step 4 - 
    We are looking for signals to buy or sell our securities, buy the ratio of their prices.
    Since the are cointegrated, and move around the mean, it is only reasonable that our signals will use features that relate to the mean value.
    - rolling mean
    - standard deviation
    - z-score
    https://medium.com/auquan/pairs-trading-data-science-7dbedafcfe5a

## Goal

Our goal involves the following:

* **Part 1**: Creating a model that test for stationarity.
* **Part 2**: Creating a model that test for cointegration.
* **Part 3**: Test and find cointegrated pairs among the dataset.
* **Part 4**: Alert to buy / sell.


Stationarity:
    A falt looking series, without trend, constant variance over time, 
    a constant autocorrelation structure over time and no periodic fluctuations.
    In our model, we will search for pairs with NO 'unit root'.
    This will suggest that the time series is not time-dependent.
    
    ** If we used non-stationary data, it doesn't say to much. The mean of it is redundent.


Cointegration, very similar to correlation, means that the ratio between two series will vary around a mean. The two series, Y and X follow the follwing:
Y = ⍺ X + e
where ⍺ is the constant ratio and e is white noise

Correlation VS Cointegration:
    Sometimes, (even almost perfectly) correlated stocks have BIG spread once they separating.
    This causes a big risk when buying / selling them.
    What we are looking for basically is two stocks that are "tied together".
    Or more 'mathematically', they are linear dependent.
    This is cointegration. 
    It is as if the stocks are bind together by an elastic band.

If two series {x_t} and {y_t} are not stationary but their linear combination U = ax_t - y_t is a stationary process, then we say {x_t} and {y-t} are cointegrated.

In general, we use Augmented Dickey-Fuller test to test cointegration.

# Assumption
If we have two stocks, X & Y, that are cointegrated in their price movements, then any divergence in the spread from 0 should be temporary and mean-reverting. Next step we will estimate the spread series.


We will create a function that caluclates the cointegration z-score of stocks.

