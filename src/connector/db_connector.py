import os

from sqlalchemy import create_engine
from src.parameters import DB_URL


def db_connect():
    env = os.environ["ENV"]

    engine = create_engine(DB_URL[env], echo=False)

    engine.connect()

    return engine
