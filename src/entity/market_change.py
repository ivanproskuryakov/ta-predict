from sqlalchemy import Column, BigInteger, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class MarketChange(Base):
    __tablename__ = 'market_change'

    id = Column(BigInteger, primary_key=True)

    exchange = Column(String)
    symbol = Column(String)

    priceChange = Column(Float(precision=32, decimal_return_scale=None))
    priceChangePercent = Column(Float(precision=32, decimal_return_scale=None))
    weightedAvgPrice = Column(Float(precision=32, decimal_return_scale=None))
    prevClosePrice = Column(Float(precision=32, decimal_return_scale=None))

    lastPrice = Column(Float(precision=32, decimal_return_scale=None))
    lastQty = Column(Float(precision=32, decimal_return_scale=None))
    bidPrice = Column(Float(precision=32, decimal_return_scale=None))
    bidQty = Column(Float(precision=32, decimal_return_scale=None))
    askPrice = Column(Float(precision=32, decimal_return_scale=None))
    askQty = Column(Float(precision=32, decimal_return_scale=None))
    openPrice = Column(Float(precision=32, decimal_return_scale=None))
    highPrice = Column(Float(precision=32, decimal_return_scale=None))
    lowPrice = Column(Float(precision=32, decimal_return_scale=None))
    volume = Column(Float(precision=32, decimal_return_scale=None))
    quoteVolume = Column(Float(precision=32, decimal_return_scale=None))

    openTime = Column(BigInteger)
    closeTime = Column(BigInteger)
    firstId = Column(BigInteger)
    lastId = Column(BigInteger)
    count = Column(BigInteger)
