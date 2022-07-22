from sqlalchemy import Column, BigInteger, String, Float, JSON, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Prediction(Base):
    __tablename__ = 'prediction'

    id = Column(BigInteger, primary_key=True)

    model = Column(String)
    started_at = Column(DateTime)

    asset = Column(String)
    market = Column(String)
    interval = Column(String)

    time = Column(String)
    price_close = Column(Float(precision=32, decimal_return_scale=None))
    price_close_next = Column(Float(precision=32, decimal_return_scale=None))
    price_close_next_diff = Column(Float(precision=32, decimal_return_scale=None))

    price_close_predicted = Column(Float(precision=32, decimal_return_scale=None))
    price_close_predicted_diff = Column(Float(precision=32, decimal_return_scale=None))

    is_match = Column(Boolean)
