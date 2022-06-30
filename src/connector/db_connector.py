import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection
from src.parameters import DB_URL


def db_connect() -> Connection:
    env = os.environ["ENV"]

    engine = create_engine(DB_URL[env], echo=False)

    engine.connect()

    return engine
