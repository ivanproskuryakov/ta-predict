import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.engine import Connection

from src.entity.ohlc import Ohlc
from src.connector.db_connector import db_connect
from src.service.util import diff_price


class OhlcRepository:
    connection: Connection
    market: str = 'BTC'
    df_len: [int] = []

    def __init__(self):
        self.connection = db_connect()

    def create(self, ohlc: Ohlc):
        with Session(self.connection) as session:
            session.add(ohlc)
            session.commit()

    def get_df_len_min(self) -> int:
        return min(self.df_len)

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
            .order_by(Ohlc.time_open.desc()) \
            .statement

        df = pd.read_sql(
            sql=sql,
            con=self.connection
        )

        # price = df['open'].iloc[-1]
        # diff = diff_price(price)
        #
        # df['open'] = df['open'].apply(lambda x: x * diff)
        # df['high'] = df['high'].apply(lambda x: x * diff)
        # df['low'] = df['low'].apply(lambda x: x * diff)
        # df['close'] = df['close'].apply(lambda x: x * diff)

        return df

    def find_down_df(
            self,
            exchange: str,
            assets_down: list[str],
            interval: str,
    ) -> pd.DataFrame:
        dfs = []

        for asset in assets_down:
            df = self.get_down_asset_desc(
                exchange=exchange,
                asset=asset,
                interval=interval
            )

            price = df[f'open_{asset}'].iloc[-1]
            diff = diff_price(price)

            df[f'open_{asset}'] = df[f'open_{asset}'].apply(lambda x: x * diff)
            df[f'high_{asset}'] = df[f'high_{asset}'].apply(lambda x: x * diff)
            df[f'low_{asset}'] = df[f'low_{asset}'].apply(lambda x: x * diff)
            df[f'close_{asset}'] = df[f'close_{asset}'].apply(lambda x: x * diff)

            self.df_len.append(len(df))
            dfs.append(df)

        df = pd.concat(dfs, axis=1)

        # print('find_down_df')
        # print(df)

        return df

    def find_btc_df(
            self,
            exchange: str,
            assets_btc: list[str],
            interval: str,
    ) -> pd.DataFrame:
        dfs = []

        for asset in assets_btc:
            df = self.get_df_btc_desc(
                exchange=exchange,
                asset=asset,
                interval=interval
            )
            price = df[f'open_BTC_{asset}'].iloc[-1]
            diff = diff_price(price)

            df[f'open_BTC_{asset}'] = df[f'open_BTC_{asset}'].apply(lambda x: x * diff)
            df[f'high_BTC_{asset}'] = df[f'high_BTC_{asset}'].apply(lambda x: x * diff)
            df[f'low_BTC_{asset}'] = df[f'low_BTC_{asset}'].apply(lambda x: x * diff)
            df[f'close_BTC_{asset}'] = df[f'close_BTC_{asset}'].apply(lambda x: x * diff)

            self.df_len.append(len(df))
            dfs.append(df)

        df = pd.concat(dfs, axis=1)

        return df

    def get_down_asset_desc(
            self,
            exchange: str,
            asset: str,
            interval: str,

    ):
        market = 'USDT'
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

            # Ohlc.quote_asset_volume.label(f'quote_asset_volume_{asset}'),
            # Ohlc.price_diff.label(f'price_diff{asset}'),
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

    def get_df_btc_desc(
            self,
            exchange: str,
            asset: str,
            interval: str,
    ):
        market = 'BTC'
        session = Session(bind=self.connection)

        sql = session.query(
            Ohlc.price_open.label(f'open_{market}_{asset}'),
            Ohlc.price_high.label(f'high_{market}_{asset}'),
            Ohlc.price_low.label(f'low_{market}_{asset}'),
            Ohlc.price_close.label(f'close_{market}_{asset}'),

            Ohlc.trades.label(f'trades_{market}_{asset}'),
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
            # ohlc.volume_maker = item['volume_maker']

            ohlc.quote_asset_volume = item['quote_asset_volume']

            data.append(ohlc)

        with Session(self.connection) as session:
            session.add_all(data)
            session.commit()
