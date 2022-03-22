from service import dumper
from parameters import assets, intervals

start_at = '90 day ago UTC'

dumper = dumper.AssetDumper()
dumper.dumpMany(assets, intervals, start_at)
