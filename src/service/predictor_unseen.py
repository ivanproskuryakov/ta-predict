import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


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
