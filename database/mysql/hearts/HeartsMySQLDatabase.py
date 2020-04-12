import mysql.connector
import json
from mysql.connector import errorcode
from HeartsMySQLVariables import CONFIG, STATE_TABLE, GAME_ID_COLUMN


class MySQLDatabase:
    """
    Database connection object
    """
    def __init__(self):
        self.cnx = get_connection()

    def get_cursor(self):
        return self.cnx.cursor()


def get_connection():
    """
    Returns a MySQL connection object

    :returns cnx: MySQL connection object
    """
    try:
        cnx = mysql.connector.connect(**CONFIG)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def query_database(query, values):
    """ Executes basic queries """
    
    db = MySQLDatabase()
    my_cursor = db.get_cursor()
    try:
        my_cursor.execute(query, values)
    except mysql.connector.Error as err:
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def insert_state(file):
    """
    The method insert_state() loads a csv file into the state table. Load data local loads the csv file that resides on the same machine
    as the mysql server. This method of inserting data is typically much faster than multiple insertions.
    
    :param file: file is the path to the csv file.
    """
    
    db = MySQLDatabase()
    my_cursor = db.get_cursor()
    try:
        query = "LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY ',' " \
                "ENCLOSED BY '\"' " \
                "LINES TERMINATED BY '\n'" \
                "IGNORE 1 LINES" \
                "(deck, action, score, game_uuid)".format(file, STATE_TABLE)
        my_cursor.execute(query)
    except mysql.connector.Error as err:
        print(err)
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
        query= "SELECT {} FROM {} WHERE {}={}".format("*", STATE_TABLE, GAME_ID_COLUMN, id_key)
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
    Tests retrieving state data from the database.
    """
    
    game_state = get_data_by_key(0)
    uuid = extract_uuid(game_state)
    state = extract_state(game_state)
    action = extract_action(game_state)
    score = extract_score(game_state)

    print(uuid)
    print(state)
    print(action)
    print(score)
