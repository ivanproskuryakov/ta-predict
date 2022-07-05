from src.repository.trade_repository import TradeRepository


def trade_create_buy():
    trade_repository = TradeRepository()

    asset = 'BTC'
    market = 'USDT'
    interval = '1h'
    price = 10000
    trades = 10000
    quantity = 0.001
    diff = 0
    order = {}

    trade = trade_repository.create_buy(
        asset=asset,
        market=market,
        trades=trades,
        interval=interval,
        diff=diff,
        price_buy=price,
        quantity=quantity,
        order=order,
    )

    return trade
