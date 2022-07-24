from src.service.backtester import BackTester

from src.parameters import assets, market

# assets = [
#     'ADA'
# ]

backtester = BackTester(
    market=market,
    interval='5m',
)

for asset in assets:
    backtester.run(
        asset=asset,
        model="gru-b-1000-48.keras",
        width=1000
    )
