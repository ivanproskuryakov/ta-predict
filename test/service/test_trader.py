from src.service.trader import Trader
from src.repository.trade_repository import TradeRepository
from src.fixture.trade import trade_create_buy


def test_order_buy():
    trader = Trader()
    trade_repository = TradeRepository()

    asset = 'BTC'
    market = 'USDT'
    interval = '1h'
    price = 10000
    amount = 0.001

    trade_buy = trader.trade_buy(
        asset,
        market,
        interval,
        price,
        amount,
    )
    trade_last = trade_repository.find_last_trade()

    assert trade_buy.id == trade_last.id
    assert trade_buy.buy_order == {}


def test_order_sell():
    trader = Trader()
    trade_repository = TradeRepository()
    trade_buy = trade_create_buy()

    price = trade_buy.buy_price * 0.01 + trade_buy.buy_price

    trader.trade_sell(
        trade=trade_buy,
        price=price,
    )

    trade_sell = trade_repository.find_id(trade_id=trade_buy.id)

    assert trade_sell.sell_price == 10100
    assert trade_sell.sell_order == {}
