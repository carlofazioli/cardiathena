import os
import glob
import shutil
import mysql
from mysql.connector import errorcode

#from database.mysql.hearts.HeartsMySQLVariables import CSV_DIR, CONFIG, GAME_TABLE, ARCHIVE_DIR, STATE_TABLE
from HeartsMySQLVariables import CSV_DIR
from HeartsMySQLVariables import ARCHIVE_DIR
from HeartsMySQLVariables import STATE_TABLE
from HeartsMySQLVariables import GAME_TABLE
from HeartsMySQLVariables import CONFIG
from HeartsMySQLVariables import SCRATCH_DIR


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


def move_files(files_list):
    for entry in files_list:
        shutil.move(entry, ARCHIVE_DIR)
    return list()


def insert_game_table():
    game_table_files = glob.glob(os.path.join(CSV_DIR, "*_gametable.csv"))
    game_table_files.sort()
    dbs = MySQLDatabase()
    my_cursor = dbs.get_cursor()
    saved_files = list()
    count = 10000

    try:
        for i, file in enumerate(game_table_files):
            query = "LOAD DATA LOCAL INFILE '{}' IGNORE INTO TABLE {} FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n'" \
                "(time, agent1, agent2, agent3, agent4, game_uuid)".format(file, GAME_TABLE)
            my_cursor.execute(query)
            saved_files.append(file)
            if i == count:
                dbs.cnx.commit()
                my_cursor.close()
                my_cursor = dbs.get_cursor()
                saved_files = move_files(saved_files)
                count = count + 10000
    except mysql.connector.Error as err:
        # Check for foreign key constraint failure
        if err.errno == 1452:
            print(err)
            pass
        # Check for duplicate game_uuid
        elif err.errno == 1062:
            pass
        else:
            print(err)
    finally:
        dbs.cnx.commit()
        my_cursor.close()
        dbs.cnx.close()
        saved_files = move_files(saved_files)


def insert_state_table():
    state_table_files = glob.glob(os.path.join(CSV_DIR, "*_statetable.csv"))
    state_table_files.sort()
    dbs = MySQLDatabase()
    my_cursor = dbs.get_cursor()
    saved_files = list()
    count = 10000
    try:
        for i, file in enumerate(state_table_files):
            query = "LOAD DATA LOCAL INFILE '{}' IGNORE INTO TABLE {} FIELDS TERMINATED BY ',' " \
                "ENCLOSED BY '\"' " \
                "LINES TERMINATED BY '\n'" \
                "(deck, action, score, game_uuid)".format(file, STATE_TABLE)
            my_cursor.execute(query)
            saved_files.append(file)
            if i == count:
                dbs.cnx.commit()
                my_cursor.close()
                my_cursor = dbs.get_cursor()
                saved_files = move_files(saved_files)
                count = count + 10000
    except mysql.connector.Error as err:
        # Check for foreign key constraint failure
        if err.errno == 1452:
            print(err)
            pass
        # Check for duplicate game_uuid
        elif err.errno == 1062:
            print(err)
            pass
        else:
            print(err)
    finally:
        dbs.cnx.commit()
        my_cursor.close()
        dbs.cnx.close()
        saved_files = move_files(saved_files)


insert_game_table()
insert_state_table()
