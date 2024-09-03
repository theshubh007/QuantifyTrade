import backtrader as bt


class MovingAverageCrossoverStrategy(bt.Strategy):
    params = dict(short_period=10, long_period=50)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.short_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.short_period
        )
        self.long_ma = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.long_period
        )
        self.order = None

    def next(self):
        if self.order:
            return  # Skip if there is already an order.

        # Buy if short MA crosses above long MA.
        if self.short_ma[0] > self.long_ma[0] and self.short_ma[-1] <= self.long_ma[-1]:
            self.order = self.buy()

        # Sell if short MA crosses below long MA.
        elif (
            self.short_ma[0] < self.long_ma[0] and self.short_ma[-1] >= self.long_ma[-1]
        ):
            self.order = self.sell()
