from service.asset_dumper import dump_many
from parameters import assets, intervals, start_at
from parameters import market

dump_many(market, assets, intervals, start_at)
