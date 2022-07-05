from binance import enums

from datetime import timedelta
from src.repository.trade_repository import TradeRepository
from src.service.klines import KLines


class TradePopulator:
    trade_repository: TradeRepository
    klines: KLines

    def __init__(self):
        self.trade_repository = TradeRepository()
        self.klines = KLines()

    def populate(self):
        trades = self.trade_repository.find_opened()

        for trade in trades:
            start_at = str(trade.interval_start - timedelta(seconds=10))

            collection = self.klines.build_klines(
                market=trade.market,
                asset=trade.asset,
                klines_type=enums.HistoricalKlinesType.SPOT,
                interval=trade.interval,
                start_at=start_at
            )

            is_interval_passed = len(collection) > 1

            if is_interval_passed:
                price_close = collection[0]['price_close']

                self.trade_repository.update(
                    trade=trade,
                    price_sell=price_close,
                    order={}
                )
