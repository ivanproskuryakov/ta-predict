from src.service.asset_dumper import dump_many
from src.parameters import assets, intervals, start_at
from src.parameters import market

dump_many(market, assets, intervals, start_at)
