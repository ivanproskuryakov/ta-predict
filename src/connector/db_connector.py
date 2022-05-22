from sqlalchemy import create_engine
from src.parameters import DB_URL


def db_connect():
    engine = create_engine(DB_URL['prod'], echo=True)

    engine.connect()

    return engine
