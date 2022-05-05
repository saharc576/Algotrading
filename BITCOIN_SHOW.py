# Raw Package
import numpy as np
import pandas as pd

#Data Source
import yfinance as yf
import time

#Data viz
import plotly.graph_objs as go

# Get Bitcoin data
if __name__ == "__main__":
    while (True):
        data1 = yf.download(tickers='BTC-USD', period = '22h', interval = '15m')
        data2 = yf.download(tickers='ETC-USD', period = '22h', interval = '15m')
        data = data1-data2
        #declare figure
        fig = go.Figure()

        #Candlestick
        fig.add_trace(go.Candlestick(x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'], name = 'market data'))

        # Add titles
        fig.update_layout(
            title='Bitcoin live share price evolution',
            yaxis_title='Bitcoin Price (kUS Dollars)')

        # X-Axes
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=6, label="6h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        #Show
        fig.show()
        time.sleep(300)

