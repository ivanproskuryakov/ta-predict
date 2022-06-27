from src.service.trader import Trader
from src.repository.trade_repository import TradeRepository


def test_order_open():
    trader = Trader()
    trade_repository = TradeRepository()

    asset = 'BTC'
    market = 'USDT'
    interval = '1h'
    price = 10000
    amount = 0.001

    trade_new = trader.trade_open(
        asset,
        market,
        interval,
        price,
        amount,
    )
    trade_last = trade_repository.find_last_trade()

    assert trade_new.id == trade_last.id
