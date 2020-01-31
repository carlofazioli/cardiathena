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
SHOW_GAMEID = "SELECT id FROM {}".format(TABLE_NAME) 
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
        self.batch = list()

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
    mycursor = db.get_cursor()
    try:
        if state is None:
            mycursor.execute(query)
            show_results(mycursor)
        else:
            values = (game_id, state)
            mycursor.execute(query, values)
    except mysql.connector.Error as err:
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        mycursor.close()
        db.cnx.close()


def show_results(cursor):
    for row in cursor.fetchall():
        print(row)


def test_db():
    query_database(CREATE_DB, None, None)
    query_database(SHOW_DATABASE, None, None)
    query_database(CREATE_TABLE, None, None)
    query_database(SHOW_TABLES, None, None)
    state = [1, 1, 4, 1, 3, 2, 2, 1, 3, 2, 4, 1, 2, 4, 2, 4, 2, 1, 1, 4, 1, 4, 1, 4, 2, 1, 3, 2, 3, 3, 4, 3, 1, 1, 4, 2, 3,
             2, 2, 3, 4, 3, 2, 3, 3, 4, 1, 2, 4, 4, 3, 3]

    query_database(INSERT_DATA, None, json.dumps(state))
    query_database(SHOW_DATA, None, None)


def initialize_db():
    query_database(CREATE_DB, None, None)
    query_database(CREATE_TABLE, None, None)


initialize_db()
#query_database(DROP_TABLE, None, None)

# test_db()
#query = "show variables like 'max_allowed_packet'"
#query = "show global status like 'Max_used_connections

#query_database(SHOW_GAMEID, "TABLE_NAME", None)
