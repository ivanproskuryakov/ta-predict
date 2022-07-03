from binance import Client, enums

from src.parameters import API_KEY, API_SECRET
from src.parameters_futures_coin import assets_futures_coin, market

client = Client(
    api_key=API_KEY,
    api_secret=API_SECRET,
)

interval = '5m'
start_at = '1610000000'
end_at = '1656110684'

for asset in assets_futures_coin:
    symbol = f'{asset}{market}'

    klines = client.get_historical_klines(
        symbol=symbol,
        interval=interval,
        start_str=start_at,
        end_str=end_at,
        klines_type=enums.HistoricalKlinesType.SPOT
    )

    print(symbol, len(klines))
