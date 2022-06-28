import pandas as pd
from datetime import datetime

from src.repository.trade_repository import TradeRepository


class TradeFinder:
    trade_repository = TradeRepository

    def __init__(self):
        self.trade_repository = TradeRepository()

    def pick_best_option(self, df: pd.DataFrame):
        return df.tail(1)

    def trade_between(
            self,
            start_at: datetime,
            end_at: datetime,
    ):
        trade = self.trade_repository.find_between(
            start_at=start_at,
            end_at=end_at,
        )

        return trade
