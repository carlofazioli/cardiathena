import os

""" Environment variables """
HOME_DIR = os.environ['HOME']
PWD_DIR = os.environ['PWD']
CSV_DIR = '{}/Argo/mysql/var/lib/mysql-files/'.format(HOME_DIR)

""" Database variables """
DB = "cardiathena_db"
SHOW_DATABASE = "SHOW DATABASES"
CREATE_DB = "CREATE DATABASE {}".format(DB)
DROP_DB = "DROP DATABASE {}".format(DB)

""" Table Column Variables """
STATE_COLUMN = "state"
ACTION_COLUMN = "action"
SCORE_COLUMN = "score"
GAME_UUID_COLUMN = "game_uuid"
PLAYER_UUID_COLUMN = "player_game_uuid"
ID_COLUMN = "id"
PLAYERS_COLUMN = "player"

""" Table variables """
SHOW_TABLES = "SHOW TABLES"
STATE_TABLE = "history_table"
PLAYER_TABLE = "player_table"
CREATE_PLAYERS_TABLE = "CREATE TABLE IF NOT EXISTS {}" \
                       "(player_game_uuid VARBINARY(32) NOT NULL, " \
                       "player JSON, " \
                       "PRIMARY KEY (player_game_uuid))".format(PLAYER_TABLE)

CREATE_STATE_TABLE = "CREATE TABLE IF NOT EXISTS {}(id INT AUTO_INCREMENT NOT NULL, " \
                     "game_uuid VARBINARY(32), " \
                     "state JSON, " \
                     "action JSON, " \
                     "score JSON," \
                     "PRIMARY KEY(id)," \
                     "FOREIGN KEY (game_uuid) REFERENCES {}({}))".format(STATE_TABLE, PLAYER_TABLE, PLAYER_UUID_COLUMN)
DROP_TABLE = "DROP TABLE {}".format(STATE_TABLE)




""" Insert queries"""
INSERT_PLAYERS = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(PLAYER_TABLE, PLAYER_UUID_COLUMN, PLAYERS_COLUMN)

""" Selection queries """
SELECT_ALL_FROM_STATE_TABLE = "SELECT * FROM {}".format(STATE_TABLE)
SELECT_ALL_FROM_PLAYER_TABLE = "SELECT * FROM {}".format(PLAYER_TABLE)
SELECT_GAME_ID = "SELECT {} FROM {} WHERE {}=".format(ID_COLUMN, STATE_TABLE, ID_COLUMN)


""" Connection Config details """
CONFIG_INITIALIZE = {
    'user': 'remote_usr',
    'password': '87bT0KDZ',
    'host': 'localhost',
    'port': '3306',
    'raise_on_warnings': True
}

CONFIG2 ={
    'user': 'remote_usr',
    'password': '87bT0KDZ',
    'host': 'localhost',
    'port': '3306',
    'db': 'cardiathena_db',
    'raise_on_warnings': True
}