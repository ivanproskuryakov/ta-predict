import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from src.service.backtester import BackTester

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

print('x_df_rescaled')
print(x_df_rescaled)

print('y_df')
print(y_df)

print('x_last')
print(x_last)

print('y_last')
print(y_last)
