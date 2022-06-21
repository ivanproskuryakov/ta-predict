import numpy as np
import pandas as pd

from sqlalchemy.orm import Session

from src.entity.ohlc import Ohlc
from src.connector.db_connector import db_connect
from src.parameters import assets_down


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html

class OhlcRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

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
        dfs = []
        df = self.get_df_full_desc(
            exchange=exchange,
            market=market,
            asset=asset,
            interval=interval
        )
        dfs.append(df)

        for asset in assets_down:
            df = self.get_df_ohlc_desc(
                exchange=exchange,
                market=market,
                asset=asset,
                interval=interval
            )
            dfs.append(df)

        df_final = pd.concat(dfs)
        df_final_asc = df_final[::-1].reset_index()

        return df_final_asc

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

            ohlc.time_open = np.round(item['time_open'], 0)
            ohlc.time_close = np.round(item['time_close'], 0)

            ohlc.time_month = item['time_month']
            ohlc.time_day = item['time_day']
            ohlc.time_hour = item['time_hour']
            ohlc.time_minute = item['time_minute']

            ohlc.price_open = item['price_open']
            ohlc.price_low = item['price_low']
            ohlc.price_high = item['price_high']
            ohlc.price_close = item['price_close']
            ohlc.price_diff = item['price_diff']

            ohlc.trades = item['trades']
            ohlc.volume = item['volume']
            ohlc.volume_taker = item['volume_taker']
            ohlc.volume_maker = item['volume_maker']

            ohlc.quote_asset_volume = item['quote_asset_volume']

            data.append(ohlc)

        with Session(self.connection) as session:
            session.add_all(data)
            session.commit()

    def get_df_ohlc_desc(
            self,
            exchange: str,
            asset: str,
            market: str,
            interval: str,

    ):
        session = Session(bind=self.connection)

        sql = session.query(
            Ohlc.price_open.label(f'open_{asset}'),
            Ohlc.price_high.label(f'high_{asset}'),
            Ohlc.price_low.label(f'low_{asset}'),
            Ohlc.price_close.label(f'close_{asset}'),

            Ohlc.trades.label(f'trades_{asset}'),
            Ohlc.volume.label(f'volume_{asset}'),
            Ohlc.volume_taker.label(f'volume_taker_{asset}'),
            Ohlc.volume_maker.label(f'volume_maker_{asset}'),
            Ohlc.quote_asset_volume.label(f'quote_asset_volume_{asset}'),

            Ohlc.price_diff.label(f'price_diff{asset}'),
        ) \
            .filter(Ohlc.exchange == exchange) \
            .filter(Ohlc.market == market) \
            .filter(Ohlc.interval == interval) \
            .filter(Ohlc.asset == asset) \
            .order_by(Ohlc.time_open.desc()) \
            .statement

        df = pd.read_sql(
            sql=sql,
            con=self.connection
        )

        return df

    def get_df_full_desc(
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
            Ohlc.volume_maker,
            Ohlc.quote_asset_volume,

            Ohlc.price_diff,

        ) \
            .filter(Ohlc.exchange == exchange) \
            .filter(Ohlc.market == market) \
            .filter(Ohlc.interval == interval) \
            .filter(Ohlc.asset == asset) \
            .order_by(Ohlc.time_open.desc()) \
            .statement

        df = pd.read_sql(
            sql=sql,
            con=self.connection
        )

        return df
