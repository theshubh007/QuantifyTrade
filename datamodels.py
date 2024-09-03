from pydantic import BaseModel
from typing import List


class DataRequest(BaseModel):
    tickers: List[str]
    start_date: str
    end_date: str
    strategy_name: str


class StrategyResult(BaseModel):
    strategy_name: str
    final_value: float
    initial_cash: float
    return_percentage: float
