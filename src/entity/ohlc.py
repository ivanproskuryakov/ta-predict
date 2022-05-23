from sqlalchemy import Column, BigInteger, String, Float
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

    price_open = Column(Float, precision=32, scale=10)
    price_high = Column(Float, precision=32, scale=10)
    price_low = Column(Float, precision=32, scale=10)
    price_close = Column(Float, precision=32, scale=10)

    avg_current = Column(Float, precision=32, scale=10)
    avg_percentage = Column(Float, precision=32, scale=10)

    trades = Column(BigInteger)
    volume = Column(BigInteger)
    volume_taker = Column(BigInteger)
    volume_maker = Column(BigInteger)

    quote_asset_volume = Column(BigInteger)
