import pandas as pd

from sklearn.preprocessing import MinMaxScaler


def scale_data(df):
    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(scaled, None, df.keys())

    return df_scaled
