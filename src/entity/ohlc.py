from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Ohlc(Base):
    __tablename__ = 'ohlc'

    id = Column(Integer, primary_key=True)

    exchange = Column(String)
    market = Column(String)
    asset = Column(String)
    interval = Column(String)

    time_open = Column(Integer)
    time_close = Column(Integer)

    price_open = Column(Float)
    price_high = Column(Float)
    price_low = Column(Float)
    price_close = Column(Float)

    avg_current = Column(Float)
    avg_percentage = Column(Float)

    trades = Column(Integer)
    volume = Column(Integer)
    volume_taker = Column(Integer)
    volume_maker = Column(Integer)

    quote_asset_volume = Column(Integer)
