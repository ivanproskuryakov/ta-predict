import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection

from src.entity.ohlc import Ohlc
from src.connector.db_connector import db_connect
from src.service.util import Utility


class OhlcRepository:
    df_len: [int] = []

    connection: Connection
    utility: Utility

    def __init__(self):
        self.connection = db_connect()
        self.utility = Utility()

    def create(self, ohlc: Ohlc):
        with Session(self.connection) as session:
            session.add(ohlc)
            session.commit()

    def get_df_predict(
            self,
            exchange: str,
            market: str,
            asset: str,
            interval: str,
    ):
        session = Session(bind=self.connection)

        sql = session.query(
            Ohlc.asset.label('asset'),
            Ohlc.time_close.label('time_close'),

            Ohlc.price_open.label('open'),
            Ohlc.price_high.label('high'),
            Ohlc.price_low.label('low'),
            Ohlc.price_close.label('close'),

            # Ohlc.time_month,
            # Ohlc.time_day,
            # Ohlc.time_hour,
            # Ohlc.time_minute,

            Ohlc.trades,
            Ohlc.volume,
            Ohlc.volume_taker,
            # Ohlc.volume_maker,
            Ohlc.quote_asset_volume,

            # Ohlc.price_diff,
            # Ohlc.price_positive,
        ) \
            .filter(Ohlc.exchange == exchange) \
            .filter(Ohlc.market == market) \
            .filter(Ohlc.interval == interval) \
            .filter(Ohlc.asset == asset) \
            .order_by(Ohlc.id.asc()) \
            .statement

        df = pd.read_sql(
            sql=sql,
            con=self.connection
        )

        return df

    def get_full_df(
            self,
            exchange: str,
            market: str,
            asset: str,
            interval: str,
    ):
        session = Session(bind=self.connection)

        sql = session.query(
            Ohlc.price_open.label('open'),
            Ohlc.price_high.label('high'),
            Ohlc.price_low.label('low'),
            Ohlc.price_close.label('close'),

            Ohlc.time_month,
            Ohlc.time_day,
            Ohlc.time_hour,
            Ohlc.time_minute,

            Ohlc.trades,
            Ohlc.volume,
            Ohlc.volume_taker,
            # Ohlc.volume_maker,
            Ohlc.quote_asset_volume,

            Ohlc.price_diff,
            Ohlc.price_positive,
        ) \
            .filter(Ohlc.exchange == exchange) \
            .filter(Ohlc.market == market) \
            .filter(Ohlc.interval == interval) \
            .filter(Ohlc.asset == asset) \
            .order_by(Ohlc.id.asc()) \
            .statement

        df = pd.read_sql(
            sql=sql,
            con=self.connection
        )

        return df

    def create_many(
            self,
            exchange: str,
            market: str,
            asset: str,
            interval: str,
            collection: []
    ):
        data = []

        for item in collection:
            ohlc = Ohlc()

            ohlc.exchange = exchange
            ohlc.interval = interval
            ohlc.market = market
            ohlc.asset = asset

            ohlc.time_open = int(item['time_open'])
            ohlc.time_close = int(item['time_close'])

            # ohlc.time_month = item['time_month']
            # ohlc.time_day = item['time_day']
            # ohlc.time_hour = item['time_hour']
            # ohlc.time_minute = item['time_minute']

            ohlc.price_open = item['price_open']
            ohlc.price_low = item['price_low']
            ohlc.price_high = item['price_high']
            ohlc.price_close = item['price_close']
            # ohlc.price_diff = item['price_diff']

            ohlc.trades = item['trades']
            ohlc.volume = item['volume']
            ohlc.volume_taker = item['volume_taker']
            # ohlc.volume_maker = item['volume_maker']

            ohlc.quote_asset_volume = item['quote_asset_volume']

            data.append(ohlc)

        with Session(self.connection) as session:
            session.add_all(data)
            session.commit()
