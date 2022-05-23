import numpy as np
import tensorflow as tf
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from src.service.dataset_builder_file import build_dataset


def make_prediction(market: str, asset: str, interval: str):
    # filepath_model = f'data/ta_{market}_{asset}_{interval}.keras'
    # filepath_model = f'data/ta_USDT_BTC_1m.keras'
    # filepath_model = f'data/ta_USDT_BTC_3m.keras'
    # filepath_model = f'data/ta_USDT_BTC_5m.keras'
    # filepath_model = f'data/ta_USDT_BTC_15m.keras'
    filepath_model = f'data/ta_USDT_BTC_30m.keras'

    x_df = build_dataset(
        market=market,
        asset=asset,
        interval=interval,
    )

    # Scale
    # ------------------------------------------------------------------------

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(x_df)

    x_df_scaled = pd.DataFrame(scaled, None, x_df.keys())
    x_df_scaled_expanded = np.expand_dims(x_df_scaled, axis=0)

    # Model
    # ------------------------------------------------------------------------

    model = tf.keras.models.load_model(filepath_model)
    y = model.predict(x_df_scaled_expanded)

    # Append
    # ------------------------------------------------------------------------

    x_df_open = pd.DataFrame(np.zeros((len(x_df), len(x_df.columns))), columns=x_df.columns)
    x_df_open['open'] = x_df['open'].values

    y_df_open = pd.DataFrame(np.zeros((len(x_df), len(x_df.columns))), columns=x_df.columns)
    y_df_open['open'] = y[0][:, 0]

    y_df_open.loc[-1] = y_df_open.loc[0]
    y_df_open = y_df_open.sort_index().reset_index(drop=True)

    # Inverse
    # ------------------------------------------------------------------------

    y_df_open_inversed = scaler.inverse_transform(y_df_open)
    y_df_open['open'] = y_df_open_inversed[:, 0]

    return (x_df_open, y_df_open)