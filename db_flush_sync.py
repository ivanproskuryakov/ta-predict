from src.entity.ohlc import Ohlc
from src.connector.db_connector import db_connect

engine = db_connect()

Ohlc.metadata.drop_all(bind=engine)
Ohlc.metadata.create_all(bind=engine)
