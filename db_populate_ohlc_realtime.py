from binance import enums

from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines

from src.parameters import assets_down
from src.parameters_usdt import assets, market
from src.parameters_btc import assets_btc, market_btc

diff_seconds = 5 * 60 * 100
end_at = 1657578600
start_at = end_at - diff_seconds

repository = OhlcRepository(-1)
klines = KLines()

exchange = 'binance'
interval = '5m'
groups = [
    {
        "market": market,
        "assets": assets,
        "type": enums.HistoricalKlinesType.SPOT
    },
    {
        "market": market,
        "assets": assets_down,
        "type": enums.HistoricalKlinesType.SPOT
    },
    {
        "market": market_btc,
        "assets": assets_btc,
        "type": enums.HistoricalKlinesType.SPOT
    },
]

for group in groups:
    for asset in group["assets"]:
        print(f'processing: {asset} {group["market"]} {interval}')

        collection = klines.build_klines(
            market=group["market"],
            asset=asset,
            klines_type=group["type"],
            interval=interval,
            start_at=str(start_at),
            end_at=str(end_at),
        )

        print(len(collection))

        repository.create_many(
            exchange,
            group["market"],
            asset,
            interval,
            collection
        )
