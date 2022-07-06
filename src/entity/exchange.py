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

    baseAssetPrecision = Column(Float(precision=32, decimal_return_scale=None))
    quotePrecision = Column(Float(precision=32, decimal_return_scale=None))
    quoteAssetPrecision = Column(Float(precision=32, decimal_return_scale=None))
    baseCommissionPrecision = Column(Float(precision=32, decimal_return_scale=None))
    quoteCommissionPrecision = Column(Float(precision=32, decimal_return_scale=None))

    lotStepSize = Column(Float(precision=32, decimal_return_scale=None))
    lotMinQty = Column(Float(precision=32, decimal_return_scale=None))
    lotMaxQty = Column(Float(precision=32, decimal_return_scale=None))
