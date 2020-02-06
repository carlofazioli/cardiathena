import mysql.connector
import json
from database.Connection import Database
from database.Variables import SELECT_ALL_DATA
from database.Variables import STATES_LIST
from database.Variables import ACTIONS_LIST
from database.Variables import SCORES_LIST

bulk_data = list()


def insert_to_database(query, game_id, state):
    """
    Establishes a connection to the database, and executes an insert query. Inserts state data into MySQL database
    :param query: predefined insert query in Variables.py
    :param state: State history, action history, and score history from a game
    """
    db = Database()
    my_cursor = db.get_cursor()
    try:
        values = (game_id, state)
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
        bulk_data.append(json.loads(data[i][1]))


def get_list(list_type):
    """
    Extracts the state history, action history, or score history from the list of decoded json objects, bulk_data.

    :param list_type: The type of history to extract.
    :returns a list of history dictionaries.
    """
    temp_list = list()
    for i in range(len(bulk_data)):
        temp = bulk_data[i][list_type]
        temp_list.append(temp)
    return temp_list


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
    create_list_of_bulk_data()
    state_list = get_list(STATES_LIST)
    action_list = get_list(ACTIONS_LIST)
    score_list = get_list(SCORES_LIST)

    print_lists(state_list)
    print_lists(action_list)
    print_lists(score_list)
