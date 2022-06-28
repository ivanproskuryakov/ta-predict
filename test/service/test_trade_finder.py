from src.service.trade_finder import TradeFinder
from src.fixture.trade import trade_create_buy


def test_find_trade():
    trade_finder = TradeFinder()
    trade_buy = trade_create_buy()

    end_at = trade_buy.interval_end + 60

    trade_finder.trade_between()