from sqlalchemy import create_engine
from src.parameters import DB_ADDRESS


def connect():
    engine = create_engine(DB_ADDRESS, echo=True)

    engine.connect()

    return engine
