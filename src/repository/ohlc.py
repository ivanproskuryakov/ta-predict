from sqlalchemy.orm import Session

from src.connector.postgres_connector import connect

connection = connect()

# create session and add objects
with Session(connection) as session:
    session.add(some_object)
    session.add(some_other_object)
    session.commit()

# https://docs.sqlalchemy.org/en/14/orm/session_basics.html
