import os
import glob
import shutil
import csv
import pandas as pd
import mysql.connector
from database.mysql.hearts.HeartsMySQLDatabase import MySQLDatabase
from database.mysql.hearts.HeartsMySQLVariables import CSV_DIR, STATE_TABLE

game_table_files = glob.glob(os.path.join(CSV_DIR, "*_gametable.csv"))
state_table_files = glob.glob(os.path.join(CSV_DIR, "*statetable.csv"))


def insert_game_table():
    dbs = MySQLDatabase()
    my_cursor = dbs.get_cursor()
    try:
        for file in game_table_files:
            query = "LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY ',' " \
                "ENCLOSED BY '\"' " \
                "LINES TERMINATED BY '\n'" \
                "IGNORE 1 LINES" \
                "(time, agent1, agent2, agent3, agent4, game_uuid)".format(file, STATE_TABLE)
            my_cursor.execute(query)
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
        for file in state_table_files:
            query = "LOAD DATA LOCAL INFILE '{}' INTO TABLE {} FIELDS TERMINATED BY ',' " \
                "ENCLOSED BY '\"' " \
                "LINES TERMINATED BY '\n'" \
                "IGNORE 1 LINES" \
                "(deck, action, score, game_uuid)".format(file, STATE_TABLE)
            my_cursor.execute(query)
    except mysql.connector.Error as err:
        print(err)
    finally:
        dbs.cnx.commit()
        my_cursor.close()
        dbs.cnx.close()


insert_game_table()
insert_state_table()
