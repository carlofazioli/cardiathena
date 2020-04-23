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

print(CSV_DIR)

game_table_files = glob.glob(os.path.join(CSV_DIR, "*_gametable.csv"))
state_table_files = glob.glob(os.path.join(CSV_DIR, "*_statetable.csv"))


with open(SCRATCH_DIR + "/{}".format("sql_logs"), 'w') as fil:
    fil.write("csv paths have been loaded\n")
print("csv paths have been loaded")

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


def insert_game_table():
    dbs = MySQLDatabase()
    my_cursor = dbs.get_cursor()
    try:
        for i, file in enumerate(game_table_files):
            query = "LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY ',' " \
                "LINES TERMINATED BY '\n'" \
                "(time, agent1, agent2, agent3, agent4, game_uuid)".format(file, GAME_TABLE)
            my_cursor.execute(query)
            shutil.move(file, ARCHIVE_DIR)

            # with open(SCRATCH_DIR + "/{}".format("sql_logs"), 'a') as fil:
            #    fil.write(file + " has been moved\n")
            if i == 10000:
                break

    except mysql.connector.Error as err:
        print(err)
    finally:
        dbs.cnx.commit()
        my_cursor.close()
        dbs.cnx.close()


def insert_state_table():
    dbs = MySQLDatabase()
    my_cursor = dbs.get_cursor()
    try:
        for i, file in enumerate(state_table_files):
            query = "LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY ',' " \
                "ENCLOSED BY '\"' " \
                "LINES TERMINATED BY '\n'" \
                "(deck, action, score, game_uuid)".format(file, STATE_TABLE)
            my_cursor.execute(query)
            shutil.move(file, ARCHIVE_DIR)           
            # with open(SCRATCH_DIR + "/{}".format("sql_logs"), 'a') as fil:
            #    fil.write(file + " has been moved\n")
            if i == 10000:
                break

    except mysql.connector.Error as err:
        print(err)
    finally:
        dbs.cnx.commit()
        my_cursor.close()
        dbs.cnx.close()


while game_table_files:
    insert_game_table()


while state_table_files:
    insert_state_table()
