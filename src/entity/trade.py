from sqlalchemy import Column, BigInteger, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Trade(Base):
    __tablename__ = 'trade'

    id = Column(BigInteger, primary_key=True)

    asset = Column(String)
    market = Column(String)
    interval = Column(String)

    buy_price = Column(Float(precision=32, decimal_return_scale=None))
    buy_quantity = Column(Float(precision=32, decimal_return_scale=None))
    buy_time = Column(BigInteger)
    buy_order = Column(JSON)

    sell_price = Column(Float(precision=32, decimal_return_scale=None))
    sell_time = Column(BigInteger)
    sell_order = Column(JSON)