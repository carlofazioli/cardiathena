DB = "state_db"
TABLE_NAME = "history"
STATE_COLUMN = "state"
ACTION_COLUMN = "action"
SCORE_COLUMN = "score"
GAME_UUID_COLUMN = "game_uuid"
ID_COLUMN = "id"

STATES_LIST = "states"
ACTIONS_LIST = "actions"
SCORES_LIST = "scores"

SHOW_DATABASE = "SHOW DATABASES"
SHOW_TABLES = "SHOW TABLES"

SELECT_ALL_DATA = "SELECT * FROM {}".format(TABLE_NAME)
SELECT_GAME_ID = "SELECT {} FROM {} WHERE {}=".format(ID_COLUMN, TABLE_NAME, ID_COLUMN)

INSERT_DATA = "INSERT INTO {} ({}, {}, {}, {}, {}) VALUES (%s, %s, %s, %s, %s)".format(TABLE_NAME,
                                                                                       ID_COLUMN,
                                                                                       GAME_UUID_COLUMN,
                                                                                       STATE_COLUMN,
                                                                                       ACTION_COLUMN,
                                                                                       SCORE_COLUMN)

CREATE_DB = "CREATE DATABASE {}".format(DB)
CREATE_TABLE = "CREATE TABLE {}" \
               "(id INT AUTO_INCREMENT NOT NULL PRIMARY KEY, game_uuid BINARY(32), state JSON, action JSON, score JSON)".format(TABLE_NAME)

DROP_DB = "DROP DATABASE {}".format(DB)
DROP_TABLE = "DROP TABLE {}".format(TABLE_NAME)

