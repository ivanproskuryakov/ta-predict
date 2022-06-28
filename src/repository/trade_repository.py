from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from src.entity.trade import Trade
from src.connector.db_connector import db_connect


class TradeRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def create_buy(
            self,
            asset: str,
            market: str,
            interval: str,
            price_buy: float,
            quantity: float,
            order: {},
    ) -> Trade:
        now = datetime.utcnow()
        interval_start = now.replace(minute=0, second=0, microsecond=0)
        interval_end = interval_start + timedelta(hours=1)

        trade = Trade()

        trade.asset = asset
        trade.market = market
        trade.interval = interval

        trade.buy_price = price_buy
        trade.buy_quantity = quantity
        trade.buy_time = now
        trade.buy_order = order

        trade.interval_start = interval_start
        trade.interval_end = interval_end

        with Session(self.connection) as session:
            session.expire_on_commit = False
            session.add(trade)
            session.commit()

        return trade

    def update(
            self,
            trade: Trade,
            price_sell: float,
            order: {},
    ) -> Trade:
        trade.sell_price = price_sell
        trade.sell_time = datetime.utcnow()
        trade.sell_order = order

        with Session(self.connection) as session:
            session.expire_on_commit = False
            session.add(trade)
            session.commit()

        return trade

    def find_last_trade(
            self,
    ) -> Trade:
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .order_by(Trade.id.desc()) \
                .first()
            session.close()

        return trade

    def find_between(
            self,
            start_at: datetime,
            end_at: datetime,
    ) -> Trade:
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .where(Trade.interval_end >= start_at) \
                .where(Trade.interval_end <= end_at) \
                .order_by(Trade.id.desc()) \
                .first()
            session.close()

        return trade

    def find_id(
            self,
            trade_id: int
    ) -> Trade:
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .where(Trade.id == trade_id) \
                .one_or_none()
            session.close()

        return trade
