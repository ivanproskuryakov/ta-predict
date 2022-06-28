from src.repository.trade_repository import TradeRepository


class TradeFinder:
    trade_repository = TradeRepository

    def __init__(self):
        self.trade_repository = TradeRepository()

    def trade_between(
            self,
            start_at: float,
            end_at: float,
    ):
        trade = self.trade_repository.find_between(
            start_at=start_at,
            end_at=end_at,
        )

        return trade
