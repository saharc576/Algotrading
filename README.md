# Pairs Trading

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


Cointegration: 
    specify co-movement of price, it is a long-term relationship

Correlation:
    specify the co-movement of return, it is a short-term relationship

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

