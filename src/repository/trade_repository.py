import time

from sqlalchemy.orm import Session
from src.entity.trade import Trade
from src.connector.db_connector import db_connect


class TradeRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def create(
            self,
            asset: str,
            market: str,
            interval: str,
            price_buy: float,
            quantity: float,
    ):
        trade = Trade()

        trade.asset = asset
        trade.market = market
        trade.interval = interval
        trade.buy_price = price_buy
        trade.buy_quantity = quantity
        trade.buy_time = time.time()

        with Session(self.connection) as session:
            session.expire_on_commit = False
            session.add(trade)
            session.commit()
            # session.close()

        return trade

    def find_last_trade(
            self,
    ):
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .order_by(Trade.id.desc()) \
                .first()
            session.close()

        return trade
