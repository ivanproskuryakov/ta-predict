from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from src.entity.trade import Trade
from src.connector.db_connector import db_connect
from src.service.util import Utility


class TradeRepository:
    connection = None
    utility: Utility

    def __init__(self):
        self.connection = db_connect()
        self.utility = Utility()

    def create_buy(
            self,
            buy_time: datetime,
            asset: str, market: str, interval: str, diff: float, trades: float,
            price_buy: float, quantity: float, order: {},
    ) -> Trade:
        interval_start = buy_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        interval_end = interval_start + timedelta(hours=1)

        m = buy_time.minute

        if interval == '30m':
            if m < 30:
                interval_start = buy_time.replace(minute=30, second=0, microsecond=0)
                interval_end = interval_start + timedelta(minutes=30)
            if m > 30:
                interval_start = buy_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                interval_end = interval_start + timedelta(minutes=30)

        if interval == '15m':
            if m == 0:
                interval_start = buy_time.replace(minute=15, second=0, microsecond=0)
                interval_end = interval_start + timedelta(minutes=15)
            if m == 15:
                interval_start = buy_time.replace(minute=30, second=0, microsecond=0)
                interval_end = interval_start + timedelta(minutes=15)
            if m == 30:
                interval_start = buy_time.replace(minute=45, second=0, microsecond=0)
                interval_end = interval_start + timedelta(minutes=15)
            if m == 45:
                interval_start = buy_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                interval_end = interval_start + timedelta(minutes=15)

            if 0 < m < 15:
                interval_start = buy_time.replace(minute=15, second=0, microsecond=0)
                interval_end = interval_start + timedelta(minutes=15)
            if 15 < m < 30:
                interval_start = buy_time.replace(minute=30, second=0, microsecond=0)
                interval_end = interval_start + timedelta(minutes=15)
            if 30 < m < 45:
                interval_start = buy_time.replace(minute=45, second=0, microsecond=0)
                interval_end = interval_start + timedelta(minutes=15)
            if m > 45:
                interval_start = buy_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                interval_end = interval_start + timedelta(minutes=15)

        if interval == '5m':
            interval_start = buy_time.replace(second=0, microsecond=0)
            interval_start = interval_start + timedelta(minutes=5)
            interval_end = interval_start + timedelta(minutes=5)

        trade = Trade()

        trade.asset = asset
        trade.market = market
        trade.interval = interval
        trade.diff_predicted = diff
        trade.trades = trades

        trade.buy_price = price_buy
        trade.buy_quantity = quantity
        trade.buy_time = buy_time
        trade.buy_order = order

        trade.interval_start = interval_start
        trade.interval_end = interval_end

        with Session(self.connection) as session:
            session.expire_on_commit = False
            session.add(trade)
            session.commit()

        return trade

    def update(self, trade: Trade, price_sell: float, order: {}) -> Trade:
        trade.sell_price = price_sell
        trade.sell_time = datetime.utcnow()
        trade.sell_order = order
        trade.diff_real = self.utility.diff_percentage(price_sell, trade.buy_price)
        trade.is_positive = trade.diff_real > 0

        with Session(self.connection) as session:
            session.expire_on_commit = False
            session.add(trade)
            session.commit()

        return trade

    def find_last_trade(self) -> Trade:
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .order_by(Trade.id.desc()) \
                .first()
            session.close()

        return trade

    def find_opened(self) -> [Trade]:
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .where(Trade.sell_price.is_(None)) \
                .order_by(Trade.id.desc()) \
                .all()
            session.close()

        return trade

    def find_between_single(self, start_at: datetime, end_at: datetime) -> Trade:
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .where(Trade.interval_end >= start_at) \
                .where(Trade.interval_end <= end_at) \
                .order_by(Trade.id.desc()) \
                .first()
            session.close()

        return trade

    def find_id(self, trade_id: int) -> Trade:
        with Session(self.connection) as session:
            trade = session.query(Trade) \
                .where(Trade.id == trade_id) \
                .one_or_none()
            session.close()

        return trade
