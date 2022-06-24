import numpy as np
import pandas as pd
import concurrent.futures

from sklearn.preprocessing import MinMaxScaler
from src.service.dataset_builder_realtime import build_dataset
from src.service.estimator import estimate_ta_fill_na


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

    df = pd.DataFrame(y[0], None, [
        'open',
    ])

    df['open'] = 0
    df['high'] = 0
    df['low'] = 0
    df['close'] = y[0]

    df['time_month'] = 0
    df['time_day'] = 0
    df['time_hour'] = 0
    df['time_minute'] = 0

    df['trades'] = 0
    df['volume'] = 0
    df['volume_taker'] = 0
    df['volume_maker'] = 0
    df['quote_asset_volume'] = 0

    df['price_diff'] = 0

    df = estimate_ta_fill_na(df)

    y_inverse = scaler.inverse_transform(df)

    y_df = pd.DataFrame(y_inverse, None, x_df.keys())

    return y_df


def data_load_parallel_all(assets: [], market: str, interval: str):
    res = []
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for asset in assets:
            futures.append(
                executor.submit(build_dataset, market, asset, interval)
            )

        for i in range(len(assets)):
            data, last_item = futures[i].result()
            res.append((assets[i], data, last_item))

    return res
