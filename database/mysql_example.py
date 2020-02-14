import mysql.connector
import json
from database.Connection import Database
from database.Variables import SELECT_ALL_DATA, SELECT_GAME_ID, ID_COLUMN, TABLE_NAME, GAME_UUID_COLUMN, STATE_COLUMN, \
    ACTION_COLUMN, SCORE_COLUMN
from database.Variables import STATES_LIST
from database.Variables import ACTIONS_LIST
from database.Variables import SCORES_LIST

bulk_data = list()


def insert_to_database(query, game_id, state, action, score):
    """
    Establishes a connection to the database, and executes an insert query. Inserts state data into MySQL database

    :param query: predefined insert query in Variables.py
    :param game_id: is the game uuid passed in as a hex and saved as binary
    :param state: state is the state for a trick
    :param action: action is the action for a trick
    :param score: is the current score for a trick
    """
    db = Database()
    my_cursor = db.get_cursor()
    try:
        values = (None, game_id, state, action, score)
        my_cursor.execute(query, values)
    except mysql.connector.Error as err:
        print("Something might be wrong: {}".format(err))
    finally:
        db.cnx.commit()
        my_cursor.close()
        db.cnx.close()


def get_bulk_data(query):
    """
    Retrieves bulk data from the database, returns a list of encoded json objects.

    :param query: predefined select all query in Variables.py
    :returns a list of encoded json objects
    """
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


def create_list_of_bulk_data():
    """
    Creates a list of decoded json objects.
    """
    data = get_bulk_data(SELECT_ALL_DATA)
    for i in range(len(data)):
        bulk_data.append(data[i])
    return bulk_data


def get_data_by_key(id_key):
    """
    Gets a "row" or a state of a game using id_key.

    :param id_key: Auto incrementing key used to identify every state
    :return data: the "row" or a state of a game from the MySQL database
    """
    db = Database()
    my_cursor = db.get_cursor()

    try:
        query= "SELECT {} FROM {} WHERE {}={}".format("*",
                                                      TABLE_NAME,
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

