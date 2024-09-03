import yfinance as yf
import backtrader as bt

# Purpose: Fetch historical market data for the specified tickers.
class MarketData:
    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.data = {}

    def fetch_data(self):
        for ticker in self.tickers:
            self.data[ticker] = yf.download(
                ticker, start=self.start_date, end=self.end_date
            )
        return self.data

