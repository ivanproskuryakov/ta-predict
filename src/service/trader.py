import pandas as pd

from src.repository.trade_repository import TradeRepository

from binance import Client
from src.entity.trade import Trade
from src.parameters import API_KEY, API_SECRET
from src.service.util import round


class Trader:
    client = Client
    market: str = 'USDT'
    trade_repository = TradeRepository
    trade_volume: float = 1000  # USDT

    def __init__(self):
        self.trade_repository = TradeRepository()
        self.client = Client(
            api_key=API_KEY,
            api_secret=API_SECRET,
        )

    def trade_buy_many(self, df: pd.DataFrame, limit: int, interval: str) -> list[Trade]:
        trades = []

        df_len = len(df)

        if limit > df_len:
            limit = df_len

        for i in range(0, limit):
            asset = df.iloc[i]['asset']
            price = round(df.iloc[i]['close_price'], 4)
            diff = round(df.iloc[i]['diff'], 4)
            quantity = round(self.trade_volume / float(price), 4)

            trade = self.trade_buy(
                asset=asset,
                market=self.market,
                interval=interval,
                price=price,
                diff=diff,
                quantity=quantity,
            )

            trades.append(trade)

        return trades

    def trade_buy(
            self,
            asset: str,
            market: str,
            interval: str,
            diff: float,
            price: float,
            quantity: float,
    ):
        # symbol = f'{asset}{market}'

        # order = self.client.create_test_order(
        #     price=price,
        #     quantity=quantity,
        #     symbol=symbol,
        #     side='BUY',
        #     type='LIMIT',
        #     timeInForce='GTC',
        #     recvWindow=5000,
        # )

        order = {}

        trade = self.trade_repository.create_buy(
            asset=asset,
            market=market,
            interval=interval,
            diff=diff,
            price_buy=price,
            quantity=quantity,
            order=order,
        )

        return trade

    def trade_sell(self, trade: Trade, price: float):
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
