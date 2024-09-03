

import backtrader as bt
class MomentumStrategy(bt.Strategy):
    params = dict(period=30, stop_loss=0.95, take_profit=1.05)

    def __init__(self):
        self.dataclose = self.datas[0].close
        self.momentum = self.dataclose - self.dataclose(-self.params.period)
        self.order = None

    def next(self):
        if self.order:
            return  # Skip if there is already an order.

        # Buy if momentum is positive.
        if self.momentum[0] > 0:
            self.order = self.buy()

        # Sell if momentum is negative.
        elif self.momentum[0] < 0:
            self.order = self.sell()

        # Implement stop-loss and take-profit logic.
        if self.position:
            if self.dataclose[0] <= self.position.price * self.params.stop_loss:
                self.sell(size=self.position.size)  # Execute stop-loss.
                self.order = None
            elif self.dataclose[0] >= self.position.price * self.params.take_profit:
                self.sell(size=self.position.size)  # Execute take-profit.
                self.order = None
