from fastapi import FastAPI, HTTPException
from datamodels import DataRequest, StrategyResult
from Marketdata import MarketData
from BacktestEngine import BacktestEngine
from Trading_Strategies.MeanReversionStrategy import MeanReversionStrategy
from Trading_Strategies.MomentumStrategy import MomentumStrategy
from MonteCarloSimulator import MonteCarloSimulator
from Trading_Strategies.MovingAverageCrossoverStrategy import (
    MovingAverageCrossoverStrategy,
)



app = FastAPI()


def fetch_data(request: DataRequest):
    try:
        market_data = MarketData(request.tickers, request.start_date, request.end_date)
        data = market_data.fetch_data()
        return {
            "status": "success",
            "data": {ticker: df.to_dict() for ticker, df in data.items()},
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# backtest is a way to test how a trading strategy would have performed in the past using historical market data.
@app.post("/run-backtest")
def run_backtest(request: DataRequest):
    try:
        market_data = MarketData(request.tickers, request.start_date, request.end_date)
        data = market_data.fetch_data()  # Fetch the market data.

        # Initialize the chosen strategy
        strategy_class = {
            "mean_reversion": MeanReversionStrategy,
            "momentum": MomentumStrategy,
            "moving_average_crossover": MovingAverageCrossoverStrategy,
        }.get(request.strategy_name, MeanReversionStrategy)

        # Run backtest
        backtest_engine = BacktestEngine(strategy_class, data)
        results, final_value = backtest_engine.run_backtest()

        # Monte Carlo Simulation
        simulator = MonteCarloSimulator(strategy_class, data)
        mean_return, std_return = simulator.run_simulation()

        initial_cash = backtest_engine.cash
        return_percentage = ((final_value - initial_cash) / initial_cash) * 100

        result_summary = StrategyResult(
            strategy_name=request.strategy_name,
            final_value=final_value,
            initial_cash=initial_cash,
            return_percentage=return_percentage,
            mean_return=mean_return,
            std_return=std_return,
        )
        return {
            "status": "success",
            "result": result_summary,
        }  # Return backtest and simulation results.
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=str(e)
        )  # Return error if backtest fails.


@app.get("/")
def read_root():
    # Provides information about available trading strategies
    strategies = {
        "mean_reversion": "Mean Reversion Strategy: Buys when the price is below the moving average and sells when it is above.",
        "momentum": "Momentum Strategy: Buys assets with positive momentum and sells those with negative momentum.",
        "moving_average_crossover": "Moving Average Crossover Strategy: Uses short-term and long-term moving averages to generate buy/sell signals.",
    }
    return {
        "message": "Welcome to the High-Level Algorithmic Trading API",
        "available_strategies": strategies,
    }
