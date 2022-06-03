from sqlalchemy import Column, BigInteger, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Exchange(Base):
    __tablename__ = 'exchange'

    id = Column(BigInteger, primary_key=True)

    exchange = Column(String)
    symbol = Column(String)

    baseAsset = Column(String)
    quoteAsset = Column(String)

    minTradeAmount = Column(Float(precision=32, decimal_return_scale=None))
    maxTradeAmount = Column(Float(precision=32, decimal_return_scale=None))
    minStepSize = Column(Float(precision=32, decimal_return_scale=None))
    minMarketStepSize = Column(Float(precision=32, decimal_return_scale=None))

    minTickSize = Column(Float(precision=32, decimal_return_scale=None))
    minPrice = Column(Float(precision=32, decimal_return_scale=None))
    maxPrice = Column(Float(precision=32, decimal_return_scale=None))

    percentPriceMultiplierUp = Column(Float(precision=32, decimal_return_scale=None))
    percentPriceMultiplierDown = Column(Float(precision=32, decimal_return_scale=None))
    minOrderValue = Column(Float(precision=32, decimal_return_scale=None))
    maxMarketOrderQty = Column(Float(precision=32, decimal_return_scale=None))
    minMarketOrderQty = Column(Float(precision=32, decimal_return_scale=None))
