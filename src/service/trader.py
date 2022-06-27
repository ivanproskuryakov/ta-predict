from src.repository.trade_repository import TradeRepository

from binance import Client
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

    def trade_open(
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

        print(order)

        trade = self.trade_repository.create(
            asset=asset,
            market=market,
            interval=interval,
            price_buy=price,
            quantity=quantity,
        )

        return trade
