import yfinance as yf
from yahoo_fin.stock_info import get_data
from datetime import datetime




def get_ticker(ticker: str):
    return yf.Ticker(ticker)


def get_interval_ticker(ticker: str, start_date="07/04/2021", end_date="", interval='1d'):
    """Interval should be in ("1d", "1wk", "1mo", "1m")
    Is able to pull data up to 3 days earlier from today"""
    today = datetime.now()
    end = end_date if end_date else datetime.strftime(today, "%d/%m/%Y")
    return get_data(ticker, start_date=start_date, end_date=end, index_as_date=True, interval=interval)


if __name__ == "__main__":
    msft = get_ticker("MSFT")
    print(msft.financials)
    print(msft.history)
    # print(get_interval_ticker("amzn"))
