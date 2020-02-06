import mysql.connector
from mysql.connector import errorcode
from database.Variables import CREATE_DB
from database.Variables import CREATE_TABLE
from database.Variables import DROP_TABLE
from database.Variables import DROP_DB
from database.Variables import SELECT_ALL_DATA
from database.Variables import SELECT_GAME_ID
from database.Variables import SHOW_TABLES
from database.Variables import SHOW_DATABASE

config = {
    'user': 'remote_usr',
    'password': '',
    #'host': '',
    'port': '3306',
    'db': 'state_db',
    'raise_on_warnings': True
}


class Database():
    """
    Database connection object
    """
    def __init__(self):
        self.cnx = connect_to_database()

    def get_cursor(self):
        return self.cnx.cursor()


def connect_to_database():
    """
    Returns a MySQL connection object

    :returns cnx: MySQL connection object
    """
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


def initialize_db():
    """
    Initializes the database. Creates a new game state database and game state table.
    """
    query_database(CREATE_DB)
    query_database(CREATE_TABLE)


def query_database(query):
    """
    Used to execute predefined basic queries, in Variables.py, without any values. Prints the results to console.
    IE 'SHOW_DATABASE' will show all the databases on the server.
    """
    db = Database()
    my_cursor = db.get_cursor()
    try:
        my_cursor.execute(query)
        show_results(my_cursor)
    except mysql.connector.Error as err:
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def show_results(cursor):
    """
    Helper method that prints the results of a query.
    """
    for row in cursor.fetchall():
        print(row)
