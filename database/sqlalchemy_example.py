from sqlalchemy import create_engine, Column, Integer, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

DATABASE_URI = 'mysql+pymysql://remote_usr:Mn1y7eId@localhost/state_db'


def create_database(database_name):
    conn = engine.connect()
    try:
        conn.execute("CREATE DATABASE " + database_name)
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


def show_db():
    print(engine.table_names())


# Interface to the database configured for database dialect and dbapi
engine = create_engine(DATABASE_URI, echo=True)
# Maintains a catalog of tables and classes relative to the Base
Base = declarative_base()


class StateActionHistory(Base):
    # Table name
    __tablename__ = 'stateactionhistory'
    # Create our table columns
    gameuuid = Column('gameuuid', Integer, primary_key=True)
    state = Column('state', Integer)
    action = Column('action', Integer)

    def __init_(self, gameuuid, state, action):
        self.gameuuid = gameuuid
        self.state = state
        self.action = action


# create_database("state_db")
# drop_database("state_db")
# drop_table('statehistory')

Base.metadata.create_all(bind=engine)

show_db()
