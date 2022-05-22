from src.entity.ohlc import Ohlc
from src.connector.postgres_connector import connect

connection = connect()

Ohlc.metadata.drop_all(bind=connection)
Ohlc.metadata.create_all(bind=connection)
