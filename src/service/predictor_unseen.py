import numpy as np
import pandas as pd
import concurrent.futures

from sklearn.preprocessing import MinMaxScaler
from src.service.dataset_builder_realtime import build_dataset, build_dataset_down, build_dataset_btc
from src.parameters import assets_down
from src.parameters_btc import assets_btc


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


def data_load_down(market: str, interval: str, start_at: str):
    dfs = []

    for asset in assets_down:
        df = build_dataset_down(
            market=market,
            asset=asset,
            interval=interval,
            start_at=start_at
        )
        dfs.append(df)

    df_final = pd.concat(dfs, axis=1)

    return df_final


def data_load_btc(market: str, interval: str, start_at: str):
    dfs = []

    for asset in assets_btc:
        df = build_dataset_btc(
            market=market,
            asset=asset,
            interval=interval,
            start_at=start_at,
        )
        dfs.append(df)

    df_final = pd.concat(dfs, axis=1)

    return df_final


def data_load_parallel_all(assets: [], market: str, interval: str):
    res = []
    futures = []
    start_at = '1 week ago UTC'

    df_down = data_load_down(market=market, interval=interval, start_at=start_at)
    df_btc = data_load_btc(market=market, interval=interval, start_at=start_at)

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for asset in assets:
            futures.append(
                executor.submit(
                    build_dataset, market, asset, interval,
                    start_at,
                    df_down,
                    df_btc
                )
            )

        for i in range(len(assets)):
            data, last_item = futures[i].result()
            res.append((assets[i], data, last_item))

    return res
