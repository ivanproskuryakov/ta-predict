from sqlalchemy.orm import Session

from src.entity.ohlc import Ohlc
from sqlalchemy.engine.base import Connectable


# https://docs.sqlalchemy.org/en/14/orm/session_basics.html

class OhlcRepository:
    connection = None

    def __init__(self, connection: Connectable):
        self.connection = connection

    def create(self, ohlc: Ohlc):
        with Session(self.connection) as session:
            session.add(ohlc)
            session.commit()

    def create_many(self, list: list[Ohlc]):
        with Session(self.connection) as session:
            session.add_all(list)
            session.commit()
