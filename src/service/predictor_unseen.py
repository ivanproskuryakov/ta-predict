import numpy as np
import pandas as pd
import ray

from sklearn.preprocessing import MinMaxScaler
from src.service.dataset_builder_realtime import build_dataset


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

    # Append
    # ------------------------------------------------------------------------

    x_df_open = pd.DataFrame(np.zeros((len(x_df), len(x_df.columns))), columns=x_df.columns)
    x_df_open['open'] = x_df['open'].values

    y_df_open = pd.DataFrame(np.zeros((len(x_df), len(x_df.columns))), columns=x_df.columns)
    y_df_open['open'] = y[0][:, 0]

    # Inverse
    # ------------------------------------------------------------------------

    y_df_open_inverse = scaler.inverse_transform(y_df_open)
    y_df_open['open'] = y_df_open_inverse[:, 0]

    return x_df_open, y_df_open


@ray.remote
def data_load(market: str, asset: str, interval: str):
    return build_dataset(
        market=market,
        asset=asset,
        interval=interval,
    )
