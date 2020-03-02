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


""" Hearts Table """
GAME_TABLE = "game"
STATE_TABLE = "state"
AGENT_TABLE = "agent"

""" Hearts Table columns """
GAME_ID_COLUMN = "game_id"
TIME_COLUMN = "time"
AGENT1_COLUMN = "agent1"
AGENT2_COLUMN = "agent2"
AGENT3_COLUMN = "agent3"
AGENT4_COLUMN = "agent4"
STATE_ID_COLUMN = "state_id"
DECK_COLUMN = "deck"
AGENT_ID_COLUMN = "agent_id"
AGENT_TYPE_COLUMN = "agent_type"
AGENT_VERSION_COLUMN = "version"

""" Hearts Table Column Variables """
STATE_COLUMN = "state"
ACTION_COLUMN = "action"
SCORE_COLUMN = "score"
GAME_UUID_COLUMN = "game_uuid"
PLAYER_UUID_COLUMN = "player_game_uuid"
ID_COLUMN = "id"
PLAYERS_COLUMN = "player"

""" Hearts Table variables """
SHOW_TABLES = "SHOW TABLES"
STATE_TABLE = "history_table"
PLAYER_TABLE = "player_table"

DROP_TABLE = "DROP TABLE {}".format(STATE_TABLE)
CREATE_GAME_TABLE = "CREATE TABLE IF NOT EXISTS {}"\
                    "({} INT8 AUTO_INCREMENT NOT NULL,"\
                    "{} TIMESTAMP,"\
                    "{} INT8," \
                    "{} INT8," \
                    "{} INT8," \
                    "{} INT8)".format(GAME_TABLE,
                                           GAME_ID_COLUMN,
                                           TIME_COLUMN,
                                           AGENT1_COLUMN,
                                           AGENT2_COLUMN,
                                           AGENT3_COLUMN,
                                           AGENT4_COLUMN)

CREATE_AGENT_TABLE = "CREATE TABLE IF NOT EXISTS {}"\
                     "({} INT8 AUTO_INCREMENT NOT NULL PRIMARY KEY,"\
                     "{} VARCHAR(45),"\
                     "{} FLOAT4)".format(AGENT_TABLE,
                                         AGENT_ID_COLUMN,
                                         AGENT_TYPE_COLUMN,
                                         AGENT_VERSION_COLUMN)

CREATE_STATE_TABLE = "CREATE TABLE IF NOT EXISTS {}"\
                     "({} INT8 AUTO_INCREMENT NOT NULL,"\
                     "{} JSON,"\
                     "{} JSON"\
                     "{} JSON"\
                     "{} INT8)".format(STATE_TABLE,
                                            STATE_ID_COLUMN,
                                            DECK_COLUMN,
                                            ACTION_COLUMN,
                                            SCORE_COLUMN,
                                            GAME_ID_COLUMN)



""" Insert queries """
INSERT_PLAYERS = "INSERT INTO {} ({},{}) VALUES (%s, %s)".format(PLAYER_TABLE, PLAYER_UUID_COLUMN, PLAYERS_COLUMN)
INSERT_GAME = "INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s, %s)".format(STATE_TABLE,
                                                                                                 GAME_ID_COLUMN,
                                                                                                 TIME_COLUMN,
                                                                                                 AGENT1_COLUMN,
                                                                                                 AGENT2_COLUMN,
                                                                                                 AGENT3_COLUMN,
                                                                                                 AGENT4_COLUMN)

INSERT_AGENT = "INSERT INTO {} ({},{},{}) VALUES (%s, %s, %s)".format(AGENT_TABLE,
                                                                      AGENT_ID_COLUMN,
                                                                      AGENT_TYPE_COLUMN,
                                                                      AGENT_VERSION_COLUMN)

INSERT_STATE = "INSERT INTO {} ({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s,)".format(STATE_TABLE,
                                                                                        STATE_ID_COLUMN,
                                                                                        DECK_COLUMN,
                                                                                        ACTION_COLUMN,
                                                                                        SCORE_COLUMN,
                                                                                        GAME_ID_COLUMN)
""" Selection queries """
SELECT_ALL_FROM_STATE_TABLE = "SELECT * FROM {}".format(STATE_TABLE)
SELECT_ALL_FROM_PLAYER_TABLE = "SELECT * FROM {}".format(PLAYER_TABLE)

SELECT_GAME_ID = "SELECT {} FROM {} WHERE {}=".format(ID_COLUMN, STATE_TABLE, ID_COLUMN)
SELECT_ALL_FROM_GAME_TABLE = "SELECT * FROM {}".format(GAME_TABLE)
SELECT_ALL_FROM_STATE_TABLE = "SELECT * FROM {}".format(STATE_TABLE)
SELECT_ALL_FROM_PLAYER_TABLE = "SELECT * FROM {}".format(AGENT_TABLE)
SELECT_GAME_ID = "SELECT {} FROM {} WHERE {}=".format(GAME_ID_COLUMN, GAME_TABLE, GAME_ID_COLUMN)

""" Connection Config details """
CONFIG_INITIALIZE = {
    'user': 'remote_usr',
    'password': '',
    'host': 'localhost',
    'port': '3306',
    'raise_on_warnings': True
}

CONFIG2 ={
    'user': 'remote_usr',
    'password': '',
    'host': 'localhost',
    'port': '3306',
    'db': 'cardiathena_db',
    'raise_on_warnings': True
}

""" Hearts Agents """
HEARTS_AGENTS = {
    "agent1": {"name": "Random", "version": "1.0"},
    "agent2": {"name": "LowLayer", "version": "1.0"}
}

