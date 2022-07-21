import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from src.service.backtester import BackTester
from src.service.util import diff_percentage

scaler = MinMaxScaler()

models = [
    ("gru-b-1000-48.keras", 1000)
]

backtester = BackTester(
    models=models,
    market='USDT',
    interval='15m',
)

x_dfs = backtester.datasets_build(asset="ETH", width=1000, scaler=scaler)
x_df = x_dfs[0]

backtester.load_model(name="gru-b-1000-48.keras")

y_df = backtester.datasets_predict(df=x_df, width=1000, scaler=scaler)

rescaled = scaler.inverse_transform(x_df)

x_df_rescaled = pd.DataFrame(rescaled, None, x_df.keys())

x_last = x_df_rescaled.iloc[-2:]
y_last = y_df.iloc[-2:]

x_diff = diff_percentage(v2=x_df_rescaled.iloc[-1]['close'], v1=x_df_rescaled.iloc[-2]['close'])
y_diff = diff_percentage(v2=y_last.iloc[-1]['close'], v1=y_last.iloc[-2]['close'])

print(x_diff, y_diff)
