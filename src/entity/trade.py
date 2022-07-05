from sqlalchemy import Column, BigInteger, String, Float, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trade'

    id = Column(BigInteger, primary_key=True)

    asset = Column(String)
    market = Column(String)
    interval = Column(String)
    interval_start = Column(DateTime)
    interval_end = Column(DateTime)

    trades = Column(Float(precision=32, decimal_return_scale=None))
    diff_predicted = Column(Float(precision=32, decimal_return_scale=None))
    diff_real = Column(Float(precision=32, decimal_return_scale=None))
    is_positive = Column(Boolean)

    buy_price = Column(Float(precision=32, decimal_return_scale=None))
    buy_quantity = Column(Float(precision=32, decimal_return_scale=None))
    buy_time = Column(DateTime)
    buy_order = Column(JSON)

    sell_price = Column(Float(precision=32, decimal_return_scale=None))
    sell_time = Column(DateTime)
    sell_order = Column(JSON)
