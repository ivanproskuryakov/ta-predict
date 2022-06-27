from src.repository.trade_repository import TradeRepository

from binance import Client
from src.entity.trade import Trade
from src.parameters import API_KEY, API_SECRET


class Trader:
    client = Client
    trade_repository = TradeRepository

    def __init__(self):
        self.trade_repository = TradeRepository()
        self.client = Client(
            api_key=API_KEY,
            api_secret=API_SECRET,
        )

    def trade_buy(
            self,
            asset: str,
            market: str,
            interval: str,
            price: float,
            quantity: float,
    ):
        symbol = f'{asset}{market}'

        order = self.client.create_test_order(
            price=price,
            quantity=quantity,
            symbol=symbol,
            side='BUY',
            type='LIMIT',
            timeInForce='GTC',
            recvWindow=5000,
        )

        trade = self.trade_repository.create_buy(
            asset=asset,
            market=market,
            interval=interval,
            price_buy=price,
            quantity=quantity,
            order=order,
        )

        return trade

    def trade_sell(
            self,
            trade: Trade,
            price: float
    ):
        symbol = f'{trade.asset}{trade.market}'

        order = self.client.create_test_order(
            price=price,
            quantity=trade.buy_quantity,
            symbol=symbol,
            side='SELL',
            type='LIMIT',
            timeInForce='GTC',
            recvWindow=5000,
        )

        trade = self.trade_repository.update(
            trade=trade,
            price_sell=price,
            order=order,
        )

        return trade
