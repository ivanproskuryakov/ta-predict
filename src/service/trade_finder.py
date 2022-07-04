import pandas as pd
from datetime import datetime

from src.repository.trade_repository import TradeRepository


class TradeFinder:
    trade_repository = TradeRepository

    def __init__(self):
        self.trade_repository = TradeRepository()

    def pick_best_options(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.query('diff > 0')

        df = df.sort_values(by=['trades'], ascending=False)

        df = df.reset_index(drop=True)

        return df

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
