from sqlalchemy import Column, BigInteger, String, Float, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ohlc(Base):
    __tablename__ = 'ohlc'

    id = Column(BigInteger, primary_key=True)

    exchange = Column(String)
    market = Column(String)
    asset = Column(String)
    interval = Column(String)

    time_open = Column(BigInteger)
    time_close = Column(BigInteger)

    price_open = Column(Float(precision=32, decimal_return_scale=None))
    price_high = Column(Float(precision=32, decimal_return_scale=None))
    price_low = Column(Float(precision=32, decimal_return_scale=None))
    price_close = Column(Float(precision=32, decimal_return_scale=None))

    trades = Column(Float(precision=32, decimal_return_scale=None))
    volume = Column(Float(precision=32, decimal_return_scale=None))
    volume_taker = Column(Float(precision=32, decimal_return_scale=None))

    quote_asset_volume = Column(Float(precision=32, decimal_return_scale=None))
