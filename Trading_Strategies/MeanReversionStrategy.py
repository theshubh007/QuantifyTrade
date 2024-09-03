import backtrader as bt

# Purpose: Defines the mean reversion trading strategy for the backtest.
class MeanReversionStrategy(bt.Strategy):
    params = dict(period=20, stop_loss=0.95, take_profit=1.05)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.sma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.period
        )
        self.order = None

    def next(self):
        if self.order:
            return

        if self.dataclose[0] < self.sma[0]:
            self.order = self.buy()

        elif self.dataclose[0] > self.sma[0]:
            self.order = self.sell()

        # Implementing stop-loss and take-profit
        if self.position:
            if self.dataclose[0] <= self.position.price * self.params.stop_loss:
                self.sell(size=self.position.size)
                self.order = None
            elif self.dataclose[0] >= self.position.price * self.params.take_profit:
                self.sell(size=self.position.size)
                self.order = None
