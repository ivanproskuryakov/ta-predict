from src.service.backtester import BackTester

models = [
    ("gru-b-1000-48.keras", 1000)
]

backtester = BackTester(
    models=models,
    market='USDT',
    interval='15m',
)

dfs, scaler = backtester.datasets_build(asset="ETH", width=1000)

backtester.load_model(name="gru-b-1000-48.keras")

y_df = backtester.datasets_predict(df=dfs[0], width=1000, scaler=scaler)

print(dfs[0])
# print(y_df)
