from sqlalchemy import create_engine, Column, Integer, String, Text, Table
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker


DB_USER = 'remote_usr'
DB_PASS = 'GH9BgFaF'
DB_HOST = 'localhost'
DB_PORT = '3306'
DATABASE = 'state_db'

DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DB_USER, DB_PASS, DB_HOST, DB_PORT, DATABASE)


def create_database(database_name):
    conn = engine.connect()
    try:
        conn.execute("CREATE DATABASE IF NOT EXISTS" + database_name)
    except SQLAlchemyError as err:
        print(err)

    conn.close()


def drop_database(database_name):
    conn = engine.connect()
    try:
        conn.execute("DROP DATABASE " + database_name)
    except SQLAlchemyError as err:
        print(err)
    conn.close()


def drop_table(table_name):
    conn = engine.connect()
    try:
        conn.execute("DROP TABLE " + table_name)
    except SQLAlchemyError as err:
        print(err)
    conn.close()


def add_data(uuid, st):
    Session = sessionmaker(bind=engine)
    session = Session()
    stateactionhistory = StateActionHistory(gameuuid=uuid, state=st)
    session.add(stateactionhistory)
    session.commit()


def get_data(uuid):
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(StateActionHistory).all()
    for row in query:
        print("gameuuid: ", row.gameuuid, "state: ", row.state, "action: ", row.action)


# Interface to the database configured for database dialect and dbapi
engine = create_engine(DATABASE_URI, echo=True)
# Maintains a catalog of tables and classes relative to the Base
Base = declarative_base()


class StateActionHistory(Base):
    # Table name
    __tablename__ = 'stateactionhistory'
    # Create our table columns
    gameuuid = Column('gameuuid', Integer, primary_key=True, nullable=False)
    state = Column('state', JSON)




Base.metadata.create_all(bind=engine)

# create_database("state_db")
# drop_database("state_db")
drop_table('stateactionhistory')