from service.dumper import AssetDumper
from parameters import assets, intervals

start_at = '6 month ago UTC'

dumper = AssetDumper()
dumper.dumpMany(assets, intervals, start_at)