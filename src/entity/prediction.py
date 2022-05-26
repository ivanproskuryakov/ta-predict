from sqlalchemy import Column, BigInteger, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Prediction(Base):
    __tablename__ = 'prediction'

    id = Column(BigInteger, primary_key=True)

    exchange = Column(String)
    market = Column(String)
    asset = Column(String)
    interval = Column(String)

    time_open = Column(BigInteger)

    price_open = Column(Float(precision=32, decimal_return_scale=None))
    price_close = Column(Float(precision=32, decimal_return_scale=None))

    prediction_price = Column(Float(precision=32, decimal_return_scale=None))
    prediction_price_error = Column(Float(precision=32, decimal_return_scale=None))
    prediction_percentage = Column(Float(precision=32, decimal_return_scale=None))
    prediction_percentage_error = Column(Float(precision=32, decimal_return_scale=None))