from sklearn.preprocessing import MinMaxScaler


def scale_data(df):
    scale = MinMaxScaler()
    df_scaled = scale.fit_transform(df)

    return df_scaled
