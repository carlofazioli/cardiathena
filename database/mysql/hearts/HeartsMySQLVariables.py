import os

""" Environment variables """
HOME_DIR = os.environ['HOME']
PWD_DIR = os.environ['PWD']

CSV_DIR = '{}/Argo/mysql/var/lib/mysql-files/'.format(HOME_DIR)
ARGO_DIR = '/scratch/$USER/mysql-files/'

""" Database variables """
DB = "cardiathena_db"

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
GAME_UUID_COLUMN = "game_uuid"
ACTION_COLUMN = "action"
SCORE_COLUMN = "score"

""" Insert queries """
INSERT_GAME = "INSERT INTO {} ({}, {}, {}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(GAME_TABLE,
                                                                                                        GAME_ID_COLUMN,
                                                                                                        TIME_COLUMN,
                                                                                                        AGENT1_COLUMN,
                                                                                                        AGENT2_COLUMN,
                                                                                                        AGENT3_COLUMN,
                                                                                                        AGENT4_COLUMN,
                                                                                                        GAME_UUID_COLUMN)

INSERT_AGENT = "INSERT INTO {} ({},{},{}) VALUES (%s, %s, %s)".format(AGENT_TABLE,
                                                                      AGENT_ID_COLUMN,
                                                                      AGENT_TYPE_COLUMN,
                                                                      AGENT_VERSION_COLUMN)

INSERT_STATE = "INSERT INTO {} ({}, {}, {}, {}, {}) VALUES(%s, %s, %s, %s, %s,)".format(STATE_TABLE,
                                                                                        STATE_ID_COLUMN,
                                                                                        DECK_COLUMN,
                                                                                        ACTION_COLUMN,
                                                                                        SCORE_COLUMN,
                                                                                        GAME_UUID_COLUMN)


""" Selection queries """
SELECT_GAME_ID = "SELECT {} FROM {} WHERE {}=".format(GAME_ID_COLUMN, GAME_TABLE, GAME_ID_COLUMN)


""" Connection Config details """
CONFIG ={
    'user': 'remote_usr',
    'password': '',
    'host': 'localhost',
    'port': '3306',
    'db': 'cardiathena_db',
    'raise_on_warnings': True
}



