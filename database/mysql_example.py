import mysql.connector
from mysql.connector import errorcode
import json

config = {
    'user': 'remote_usr',
    'password': '',
    'host': '',
    'port': '3306',
    'db': 'state_db',
    'raise_on_warnings': True
}

DB = "state_db"
TABLE_NAME = "history"
STATE_COLUMN = "state"

ID_COLUMN = "id"
SHOW_DATABASE = "SHOW DATABASES"
SHOW_TABLES = "SHOW TABLES"
SHOW_DATA = "SELECT * FROM {}".format(TABLE_NAME)
SHOW_GAME_ID = "SELECT id FROM {}".format(TABLE_NAME)

INSERT_DATA = "INSERT INTO {} ({}, {}) VALUES (%s, %s)".format(TABLE_NAME, ID_COLUMN, STATE_COLUMN)

SET_INITIAL = "ALTER TABLE {} AUTO_INCREMENT=1".format(TABLE_NAME)
CREATE_TABLE = "CREATE TABLE {}" \
               "(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, state JSON)".format(TABLE_NAME)
CREATE_DB = "CREATE DATABASE {}".format(DB)
DROP_DB = "DROP DATABASE {}".format(DB)
DROP_TABLE = "DROP TABLE {}".format(TABLE_NAME)


class Database():

    def __init__(self):
        self.cnx = connect_to_database()

    def get_cursor(self):
        return self.cnx.cursor()


def connect_to_database():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def query_database(query, game_id, state):
    db = Database()
    my_cursor = db.get_cursor()
    try:
        if state is None:
            my_cursor.execute(query)
            show_results(my_cursor)
        else:
            values = (game_id, state)
            my_cursor.execute(query, values)
    except mysql.connector.Error as err:
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def get_bulk_data(query):
    db = Database()
    my_cursor = db.get_cursor()
    try:
        my_cursor.execute(query)
        data_results = list()
        for row in my_cursor.fetchall():
            data_results.append(row)
        return data_results
    except mysql.connector.Error as err:
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def show_results(cursor):
    for row in cursor.fetchall():
        print(row)


def initialize_db():
    query_database(CREATE_DB, None, None)
    query_database(CREATE_TABLE, None, None)


# initialize_db()
# query_database(DROP_DB, None, None)

# test_db()
# query = "show variables like 'max_allowed_packet'"
# query = "show global status like 'Max_used_connections

query_database(SHOW_DATA, "TABLE_NAME", None)
