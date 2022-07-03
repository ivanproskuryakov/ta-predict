import pandas as pd
import concurrent.futures

from src.service.estimator import estimate_ta_fill_na
from src.service.klines import KLines
from src.service.util import diff_percentage


class DatasetBuilderAPI:
    assets: [str]
    assets_down: [str]
    assets_btc: [str]
    interval: str
    market: str
    start_at: str

    def __init__(
            self,
            assets: [str],
            assets_down: [str],
            assets_btc: [str],
            interval: str,
            market: str,
    ):
        self.assets = assets
        self.assets_down = assets_down
        self.assets_btc = assets_btc
        self.interval = interval
        self.market = market
        self.start_at = '1 week ago UTC'

    def build_dataset_all(self) -> list:
        res = []
        futures = []

        df_down = self.__data_load_down()
        df_btc = self.__data_load_btc()

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for asset in self.assets:
                futures.append(
                    executor.submit(
                        self.__build_dataset_full,
                        asset, df_down, df_btc
                    )
                )

            for i in range(len(self.assets)):
                data, last_item = futures[i].result()
                res.append((self.assets[i], data, last_item))

        return res

    def __build_dataset_full(
            self,
            asset: str,
            df_down: pd.DataFrame,
            df_btc: pd.DataFrame
    ):
        klines = KLines()
        prepared = []

        collection = klines.build_klines(
            self.market,
            asset,
            self.interval,
            self.start_at,
        )

        for item in collection:
            diff = diff_percentage(item['price_close'], item['price_open'])

            prepared.append([
                item['price_open'],
                item['price_high'],
                item['price_low'],
                item['price_close'],

                item['time_month'],
                item['time_day'],
                item['time_hour'],
                item['time_minute'],

                item['trades'],
                item['volume'],
                item['volume_taker'],
                item['volume_maker'],
                item['quote_asset_volume'],

                diff,
            ])

        df_ohlc = pd.DataFrame(prepared, None, [
            'open',
            'high',
            'low',
            'close',

            'time_month',
            'time_day',
            'time_hour',
            'time_minute',

            'trades',
            'volume',
            'volume_taker',
            'volume_maker',
            'quote_asset_volume',

            'price_diff',
        ])

        df = pd.concat([df_ohlc, df_down, df_btc], axis=1)
        df = estimate_ta_fill_na(df)

        return df, item

    def __build_dataset_down(self, asset: str) -> pd.DataFrame:
        klines = KLines()
        prepared = []

        collection = klines.build_klines(
            self.market,
            asset,
            self.interval,
            self.start_at
        )

        for item in collection:
            prepared.append([
                item['price_open'],
                item['price_high'],
                item['price_low'],
                item['price_close'],

                item['trades'],
                item['volume'],
                item['volume_taker'],
                item['volume_maker'],
            ])

        df = pd.DataFrame(prepared, None, [
            f'open_{asset}',
            f'high_{asset}',
            f'low_{asset}',
            f'close_{asset}',

            f'trades_{asset}',
            f'volume_{asset}',
            f'volume_taker_{asset}',
            f'volume_maker_{asset}',
        ])

        return df

    def build_dataset_btc(self, asset: str) -> pd.DataFrame:
        klines = KLines()
        prepared = []

        collection = klines.build_klines(
            self.market,
            asset,
            self.interval,
            self.start_at
        )

        for item in collection:
            prepared.append([
                item['price_open'],
                item['price_close'],

                item['trades'],
            ])

        df = pd.DataFrame(prepared, None, [
            f'open_{asset}',
            f'close_{asset}',

            f'trades_{asset}',
        ])

        return df

    def __data_load_down(self,):
        res = []
        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for asset in self.assets_down:
                futures.append(
                    executor.submit(
                        self.__build_dataset_down,
                        asset,
                    )
                )

            for i in range(len(self.assets_down)):
                data = futures[i].result()
                res.append(data)

        df_final = pd.concat(res, axis=1)

        return df_final

    def __data_load_btc(self):
        res = []
        futures = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            for asset in self.assets_btc:
                futures.append(
                    executor.submit(
                        self.build_dataset_btc,
                        asset,
                    )
                )

            for i in range(len(self.assets_btc)):
                data = futures[i].result()
                res.append(data)

        df_final = pd.concat(res, axis=1)

        return df_final

    # file = open('data/ohlc.json', 'w')
    # file.write(json.dumps(collection))
    #
    # file = open('data/ohlc.json', 'r')
    # collection = json.loads(file.read())
