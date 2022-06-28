import numpy as np
import pandas as pd
import ray

from sklearn.preprocessing import MinMaxScaler
from src.service.dataset_builder_realtime import build_dataset, build_dataset_down
from src.service.estimator import estimate_ta_fill_na
from src.parameters import assets_down


def make_prediction(x_df, model):
    # Scale
    # ------------------------------------------------------------------------
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(x_df)

    x_df_scaled = pd.DataFrame(scaled, None, x_df.keys())
    x_df_scaled_expanded = np.expand_dims(x_df_scaled, axis=0)

    # Predict
    # ------------------------------------------------------------------------
    y = model.predict(x_df_scaled_expanded, verbose=0)

    df = pd.DataFrame(y[0], None, [
        'open',
        'high',
        'low',
        'close',

        # 'time_month',
        # 'time_day',
        # 'time_hour',
        # 'time_minute',

        # 'avg_percentage',
        # 'avg_current',

        'trades',
        'volume',
        'volume_taker',
        'volume_maker',
        'quote_asset_volume',
        # 'epoch',

        'price_diff',
    ])

    df = estimate_ta_fill_na(df)

    y_inverse = scaler.inverse_transform(df)

    y_df = pd.DataFrame(y_inverse, None, x_df.keys())

    return y_df


def make_prediction_ohlc_close(x_df, model):
    # Scale
    # ------------------------------------------------------------------------
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(x_df)

    x_df_scaled = pd.DataFrame(scaled, None, x_df.keys())
    x_df_scaled_expanded = np.expand_dims(x_df_scaled, axis=0)

    # Predict
    # ------------------------------------------------------------------------
    y = model.predict(x_df_scaled_expanded, verbose=0)

    df = pd.DataFrame(0, index=np.arange(len(y[0])), columns=x_df.keys())

    df['close'] = y[0]

    y_inverse = scaler.inverse_transform(df)

    y_df = pd.DataFrame(y_inverse, None, x_df.keys())

    return y_df


@ray.remote
def data_load_remote(asset: str, market: str, interval: str, df_down: pd.DataFrame):
    data, last_item = build_dataset(
        market=market,
        asset=asset,
        interval=interval,
        df_down=df_down
    )

    return asset, data, last_item


def data_load_down(market: str, interval: str):
    dfs = []

    for asset in assets_down:
        df = build_dataset_down(
            market=market,
            asset=asset,
            interval=interval,
        )
        dfs.append(df)

    df_final = pd.concat(dfs, axis=1)

    return df_final


def data_load_parallel_all(assets: [], market: str, interval: str):
    fns = []

    df_down = data_load_down(market=market, interval=interval)

    for asset in assets:
        fns.append(data_load_remote.remote(asset, market, interval, df_down))

    return ray.get(fns)
