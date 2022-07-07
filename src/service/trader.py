import pandas as pd

from datetime import datetime
from binance import Client

from src.repository.trade_repository import TradeRepository
from src.repository.exchange_repository import ExchangeRepository

from src.entity.trade import Trade
from src.parameters import API_KEY, API_SECRET
from src.service.util import round, get_precision


class Trader:
    client = Client
    market: str = 'USDT'
    trade_volume: float = 1000  # USDT

    trade_repository: TradeRepository
    exchange_repository: ExchangeRepository

    def __init__(self):
        self.trade_repository = TradeRepository()
        self.exchange_repository = ExchangeRepository()
        self.client = Client(
            api_key=API_KEY,
            api_secret=API_SECRET,
        )

    def trade_buy_many(self, df: pd.DataFrame, limit: int, interval: str, buy_time: datetime) -> list[Trade]:
        trades = []
        df_len = len(df)

        if limit > df_len:
            limit = df_len

        for i in range(0, limit):
            asset = df.iloc[i]['asset']

            exchange = self.exchange_repository.get_market_asset(
                market=self.market,
                asset=asset
            )
            # precision = get_precision(exchange.lotStepSize)

            price_close = round(df.iloc[i]['close_price'], 8)
            diff = round(df.iloc[i]['diff'], 4)
            trades_amount = round(df.iloc[i]['trades'], 0)
            quantity = round(self.trade_volume / float(price_close), 4)

            trade = self.trade_buy(
                buy_time=buy_time,
                asset=asset,
                market=self.market,
                trades=trades_amount,
                interval=interval,
                price=price_close,
                diff=diff,
                quantity=quantity,
            )

            trades.append(trade)

        return trades

    def trade_buy(
            self,
            buy_time: datetime,
            asset: str,
            market: str,
            interval: str,
            trades: float,
            diff: float,
            price: float,
            quantity: float,
    ):
        symbol = f'{asset}{market}'

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
            buy_time=buy_time,
            asset=asset,
            market=market,
            interval=interval,
            trades=trades,
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
