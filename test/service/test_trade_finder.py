import json
import pandas as pd
from datetime import timedelta

from src.service.trade_finder import TradeFinder
from src.fixture.trade import trade_create_buy
from src.service.reporter import Reporter
from fixture.prediction import load_predictions


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


def test_pick_best_option():
    reporter = Reporter()
    trade_finder = TradeFinder()

    data = load_predictions()

    df = reporter.report_build(data=data)

    best = trade_finder.pick_best_option(df)

    assert best['asset'] == 'BTC'
