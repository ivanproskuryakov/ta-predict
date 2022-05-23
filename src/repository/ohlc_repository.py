import numpy as np
import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Connectable

from src.entity.ohlc import Ohlc


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html

class OhlcRepository:
    connection = None

    def __init__(self, connection: Connectable):
        self.connection = connection

    def create(self, ohlc: Ohlc):
        with Session(self.connection) as session:
            session.add(ohlc)
            session.commit()

    def find_all_with_df(
            self,
            exchange: str,
            market: str,
            asset: str,
            interval: str,
    ):
        list = []

        with Session(self.connection) as session:
            collection = session.query(Ohlc) \
                .filter(Ohlc.exchange == exchange) \
                .filter(Ohlc.market == market) \
                .filter(Ohlc.interval == interval) \
                .filter(Ohlc.interval == interval) \
                .filter(Ohlc.asset == asset) \
                .order_by(Ohlc.time_open) \
                .all()

            for item in collection:
                list.append([
                    item.price_open,
                    item.price_high,
                    item.price_low,
                    item.price_close,

                    item.avg_percentage,
                    item.avg_current,

                    item.trades,
                    item.volume,
                    item.volume_taker,
                    item.volume_maker,

                    item.quote_asset_volume,
                    # datetime.utcfromtimestamp(collection[i]['time_open']),
                ])

        df = pd.DataFrame(list, None, [
            'open',
            'high',
            'low',
            'close',

            'avg_percentage',
            'avg_current',

            'trades',
            'volume',
            'volume_taker',
            'volume_maker',

            'quote_asset_volume',
            # 'epoch',
        ])

        return df

    def create_many(
            self,
            exchange: str,
            market: str,
            asset: str,
            interval: str,
            collection: []
    ):
        list = []

        for item in collection:
            ohlc = Ohlc()

            ohlc.exchange = exchange
            ohlc.interval = interval
            ohlc.market = market
            ohlc.asset = asset

            ohlc.time_open = np.round(item['time_open'], 0)
            ohlc.time_close = np.round(item['time_close'], 0)

            ohlc.price_open = item['price_open']
            ohlc.price_low = item['price_low']
            ohlc.price_high = item['price_high']
            ohlc.price_close = item['price_close']

            ohlc.avg_current = item['avg_current']
            ohlc.avg_percentage = item['avg_percentage']

            ohlc.trades = item['trades']
            ohlc.volume = item['volume']
            ohlc.volume_taker = item['volume_taker']
            ohlc.volume_maker = item['volume_maker']

            ohlc.quote_asset_volume = item['quote_asset_volume']

            list.append(ohlc)

        with Session(self.connection) as session:
            session.add_all(list)
            session.commit()
