from datetime import datetime, timedelta

from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines

exchange = 'binance'
market = 'USDT'

# end_at = datetime.utcnow()
# start_at = end_at - timedelta(365 * 8)  # 8 years

start_at = '1404219084'
end_at = '1656510684'

repository = OhlcRepository()
klines = KLines()

interval = '5m'
assets = [
    'BTC',
    "BNB",
    "NEO",
    "LTC",
    "ADA",
    "XRP",
    "EOS",

    "BTCUP",
    "BTCDOWN",
    "ETHUP",
    "ETHDOWN",
    "ADAUP",
    "ADADOWN",
    "LINKUP",
    "LINKDOWN",
    "BNBUP",
    "BNBDOWN",
    "TRXUP",
    "TRXDOWN",
    "XRPUP",
    "XRPDOWN",
    "DOTUP",
    "DOTDOWN",
]

for asset in assets:
    print(f'processing: {asset} {interval}')
    collection = klines.build_klines(
        market,
        asset,
        interval,
        start_at,
        end_at,
    )

    print(len(collection))

    repository.create_many(exchange, market, asset, interval, collection)
