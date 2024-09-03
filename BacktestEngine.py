import backtrader as bt

# Purpose: Manages the backtesting process using historical data and a trading strategy.
class BacktestEngine:
    def __init__(self, strategy, data, cash=100000):
        self.strategy = strategy
        self.data = data
        self.cash = cash

    def run_backtest(self):
        cerebro = bt.Cerebro()
        cerebro.broker.set_cash(self.cash)
        for ticker, df in self.data.items():
            cerebro.adddata(bt.feeds.PandasData(dataname=df), name=ticker)
        cerebro.addstrategy(self.strategy)
        result = cerebro.run()
        return result, cerebro.broker.getvalue()
