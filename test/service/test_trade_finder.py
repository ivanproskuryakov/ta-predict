import json
import pandas as pd
from datetime import timedelta

from src.service.trade_finder import TradeFinder
from src.fixture.trade import trade_create_buy
from src.service.reporter import Reporter


def test_find_trade_positive():
    trade_finder = TradeFinder()
    trade_buy = trade_create_buy()

    time_from = trade_buy.interval_end - timedelta(minutes=15)
    time_end = trade_buy.interval_end

    trade = trade_finder.trade_between(time_from, time_end)

    assert trade.id == trade_buy.id


def test_find_trade_negative():
    trade_finder = TradeFinder()
    trade_buy = trade_create_buy()

    time_from = trade_buy.interval_end - timedelta(minutes=25)
    time_end = trade_buy.interval_end - timedelta(minutes=15)

    trade = trade_finder.trade_between(time_from, time_end)

    assert trade is None


def test_pick_best_trade():
    reporter = Reporter()
    trade_finder = TradeFinder()

    assets = [
        'BTC',
        'ETH',
        'IOTA',
        'ONT',
        'TUSD',
        'XLM',
    ]
    data = []

    for asset in assets:
        file = open(f'test/fixture/prediction/prediction_{asset}_x_df.json', 'r')
        x_df = pd.DataFrame.from_dict(json.loads(file.read()))
        file = open(f'test/fixture/prediction/prediction_{asset}_y_df.json', 'r')
        y_df = pd.DataFrame.from_dict(json.loads(file.read()))
        file = open(f'test/fixture/prediction/prediction_{asset}_last_item.json', 'r')
        last_item = json.loads(file.read())

        data.append((asset, last_item, x_df, y_df))

    df = reporter.build_report(data=data)

    best = trade_finder.pick_best_option(df)

    assert best.iloc[-1]['asset'] == 'BTC'
