from sqlalchemy.orm import Session

from src.entity.ohlc import Ohlc


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html

class OhlcRepository:
    connection = None

    def __init__(self, connection):
        self.connection = connection

    def add(self,
            exchange: str,
            interval: str,

            market: str,
            asset: str,

            time_open: int,
            time_close: int,

            price_open: float,
            price_low: float,
            price_high: float,
            price_close: float,

            avg_current: float,
            avg_percentage: float,
            trades: int,
            volume: int,
            volume_taker: int,
            volume_maker: int,
            quote_asset_volume: int,
            ):
        with Session(self.connection) as session:
            ohlc = Ohlc()

            ohlc.exchange = exchange
            ohlc.interval = interval
            ohlc.market = market
            ohlc.asset = asset

            ohlc.time_open = time_open
            ohlc.time_close = time_close

            ohlc.price_open = price_open
            ohlc.price_low = price_low
            ohlc.price_high = price_high
            ohlc.price_close = price_close

            ohlc.avg_current = avg_current
            ohlc.avg_percentage = avg_percentage

            ohlc.trades = trades
            ohlc.volume = volume
            ohlc.volume_taker = volume_taker
            ohlc.volume_maker = volume_maker

            ohlc.quote_asset_volume = quote_asset_volume

            session.add(ohlc)
            session.commit()
