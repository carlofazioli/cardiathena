import mysql.connector
import json
from mysql.connector import errorcode
from database.MySQLVariables import CREATE_DB
from database.MySQLVariables import CREATE_PLAYERS_TABLE
from database.MySQLVariables import STATE_TABLE
from database.MySQLVariables import ID_COLUMN
from database.MySQLVariables import SELECT_ALL_FROM_PLAYER_TABLE
from database.MySQLVariables import SELECT_ALL_FROM_STATE_TABLE
from database.MySQLVariables import CREATE_STATE_TABLE
from database.MySQLVariables import DROP_TABLE
from database.MySQLVariables import DROP_DB
from database.MySQLVariables import SELECT_GAME_ID
from database.MySQLVariables import SHOW_TABLES
from database.MySQLVariables import SHOW_DATABASE
from database.MySQLVariables import CONFIG_INITIALIZE
from database.MySQLVariables import CONFIG2


class MySQLDatabase:
    """
    Database connection object
    """
    def __init__(self):
        if get_connection() is None:
            initialize_db()
        self.cnx = get_connection()

    def get_cursor(self):
        return self.cnx.cursor()


def get_connection():
    """
    Returns a MySQL connection object

    :returns cnx: MySQL connection object
    """
    try:
        cnx = mysql.connector.connect(**CONFIG2)
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
    try:
        cnx = mysql.connector.connect(**CONFIG_INITIALIZE)
        my_cursor = cnx.cursor()
        my_cursor.execute(CREATE_DB)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)
    finally:
        cnx.commit()
        my_cursor.close()
        cnx.close()


def initialize_table():
    query_database(CREATE_PLAYERS_TABLE)
    query_database(CREATE_STATE_TABLE)


def query_database(query):
    """
    Used to execute predefined basic queries, in MySQLVariables.py, without any values. Prints the results to console.
    IE 'SHOW_DATABASE' will show all the databases on the server.
    """
    db = MySQLDatabase()
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


def insert_state(query, game_uuid, state, action, score):
    """
    Establishes a connection to the database, and executes an insert query. Inserts state data into MySQL database

    :param query: predefined insert query in MySQLVariables.py
    :param game_uuid: is the game uuid passed in as a hex and saved as binary
    :param state: state is the state for a trick
    :param action: action is the action for a trick
    :param score: is the current score for a trick
    """
    db = MySQLDatabase()
    my_cursor = db.get_cursor()
    try:
        values = (None, game_uuid, state, action, score)
        my_cursor.execute(query, values)
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            return False
        else:
            print(err)
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def insert_players(query, game_uuid, players):
    """
    Establishes a connection to the database, and executes an insert query. Inserts state data into MySQL database

    :param query: predefined insert query in MySQLVariables.py
    :param game_uuid: is the game uuid passed in as a hex and saved as binary
    :param players: is the players that participated in a game
    """
    db = MySQLDatabase()
    my_cursor = db.get_cursor()
    try:
        values = (game_uuid, players)
        my_cursor.execute(query, values)
        return True
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_NO_SUCH_TABLE:
            return False
        else:
            print(err)
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def get_data_by_key(id_key):
    """
    Gets a "row" or a state of a game using id_key.

    :param id_key: Auto incrementing key used to identify every state
    :return data: the "row" or a state of a game from the MySQL database
    """
    db = MySQLDatabase()
    my_cursor = db.get_cursor()

    try:
        query= "SELECT {} FROM {} WHERE {}={}".format("*",
                                                      STATE_TABLE,
                                                      ID_COLUMN,
                                                      id_key)
        my_cursor.execute(query)
        data = my_cursor.fetchall()
        return data
    except mysql.connector.Error as err:
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def extract_uuid(game_state):
    """
    Extracts the game uuid from the queried data

    :return: game uuid
    """
    return game_state[0][1].decode("utf-8")


def extract_state(game_state):
    """
    Extracts the game state from the queried data

    :return: game uuid
    """
    return json.loads(game_state[0][2])


def extract_action(game_state):
    """
    Extracts the agent action tied to a state from the queried data

    :return: agent action
    """
    return json.loads(game_state[0][3])


def extract_score(game_state):
    """
    Extracts the game uuid from the queried data

    :return: score
    """
    return json.loads(game_state[0][4])


def print_lists(list):
    """
    Prints out the list of history dictionaries.
    """
    for x in range(len(list)):
        print(list[x])


def test_get_data_example():
    """
    Tests retrieving history data from the database.
    """
    game_state = get_data_by_key(10)
    uuid = extract_uuid(game_state)
    state = extract_state(game_state)
    action = extract_action(game_state)
    score = extract_score(game_state)

    print(uuid)
    print(state)
    print(action)
    print(score)


#query_database(DROP_DB)
#query_database(CREATE_PLAYERS_TABLE)
#query_database(CREATE_STATE_TABLE)
#query_database(SHOW_DATABASE)
#query_database(SHOW_TABLES)
#query_database(SELECT_ALL_FROM_PLAYER_TABLE)
#query_database(SELECT_ALL_FROM_STATE_TABLE)