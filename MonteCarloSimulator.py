import numpy as np
from BacktestEngine import BacktestEngine


class MonteCarloSimulator:
    def __init__(self, strategy, data, num_simulations=1000):
        self.strategy = strategy
        self.data = data
        self.num_simulations = num_simulations

    def run_simulation(self):
        results = []
        for _ in range(self.num_simulations):
            # Run a backtest with a randomly adjusted strategy or market conditions.
            backtest_engine = BacktestEngine(self.strategy, self.data)
            _, final_value = backtest_engine.run_backtest()
            results.append(final_value)
        return np.mean(results), np.std(
            results
        )  # Return mean and standard deviation of results.
