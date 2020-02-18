DB = "cardiathena_db"
STATE_TABLE = "history_table"
PLAYER_TABLE = "player_table"
STATE_COLUMN = "state"
ACTION_COLUMN = "action"
SCORE_COLUMN = "score"
GAME_UUID_COLUMN = "game_uuid"
PLAYER_UUID_COLUMN = "player_game_uuid"
ID_COLUMN = "id"
PLAYERS_COLUMN = "player"

SHOW_DATABASE = "SHOW DATABASES"
SHOW_TABLES = "SHOW TABLES"

SELECT_ALL_FROM_STATE_TABLE = "SELECT * FROM {}".format(STATE_TABLE)
SELECT_ALL_FROM_PLAYER_TABLE = "SELECT * FROM {}".format(PLAYER_TABLE)
SELECT_GAME_ID = "SELECT {} FROM {} WHERE {}=".format(ID_COLUMN, STATE_TABLE, ID_COLUMN)

INSERT_STATE = "INSERT INTO {} ({}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s)".format(STATE_TABLE,
                                                                                        ID_COLUMN,
                                                                                        GAME_UUID_COLUMN,
                                                                                        STATE_COLUMN,
                                                                                        ACTION_COLUMN,
                                                                                        SCORE_COLUMN)
INSERT_PLAYERS = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(PLAYER_TABLE, PLAYER_UUID_COLUMN, PLAYERS_COLUMN)

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

CREATE_DB = "CREATE DATABASE {}".format(DB)


DROP_DB = "DROP DATABASE {}".format(DB)
DROP_TABLE = "DROP TABLE {}".format(STATE_TABLE)

CONFIG_INITIALIZE = {
    'user': 'remote_usr',
    'password': '',
    #'host': '',
    'port': '3306',
    'raise_on_warnings': True
}

CONFIG2 ={
    'user': 'remote_usr',
    'password': '',
    # 'host': '',
    'port': '3306',
    'db': 'cardiathena_db',
    'raise_on_warnings': True
}