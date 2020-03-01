import json
import uuid
import csv
from base import GameManager
from adjudicator.hearts_adjudicator import HeartsAdjudicator
from adjudicator.state import HeartsState
from agent.RandomHeartsAgent import RandomHeartsAgent
from agent.LowLayer import LowLayer
from database import MySQLDatabase as db
from database.MySQLVariables import INSERT_PLAYERS, CSV_DIR

# Create the players, the adjudicator, and the game object.
game_uuid = uuid.uuid4().hex
agent_1 = RandomHeartsAgent()
agent_2 = RandomHeartsAgent()
agent_3 = LowLayer()
agent_4 = RandomHeartsAgent()
adj = HeartsAdjudicator()
state = HeartsState()
agent_list = [0, agent_1, agent_2, agent_3, agent_4]
json_agent_list = list()
game = GameManager(agent_list,
                   adjudicator=adj,
                   state=state)


def save_agents():
    """
    The save_agents() method saves the agent types ie Random Hearts Agent to the players table. It attempts to insert
    into the database. However if insert_players method returns false, the table has not been initialized. It will then
    initialize the tables and insert the agent types.

    """
    # Remove 0 from agent_list
    for agent in agent_list:
        if agent is not 0:
            json_agent_list.append(str(agent))

    # Insert agents to the players table. Initialize tables if not already initialized.
    if db.insert_players(INSERT_PLAYERS, game_uuid, json.dumps(json_agent_list)) is False:
        db.initialize_table()
        db.insert_players(INSERT_PLAYERS, game_uuid, json.dumps(json_agent_list))


def process_state_data():
    """
    The process_state_data() method processes the state data to be stored in the MySQL database. The state data includes
    location of the cards: deck (numPy array converted to a python list), player actions: action, scores, and a game
    uuid. The method calls save_game() from the game manager which returns a list of dictionaries which contains
    deck, action, and score. In order to reduce overhead with multiple insertions, game state data is writen to a
    csv file which is then inserted into the database.

    """
    # Get state_data, list of dictionaries, from game manager's save_game()
    state_data = game.save_game()

    # Process state_data, insert into database
    directory = CSV_DIR + "{}.csv".format(game_uuid)
    with open(directory, 'w') as file:
        writer = csv.writer(file, lineterminator='\n',)
        writer.writerow(["game_uuid", "deck", "action", "score"])
        for data in state_data:
            deck = data["deck"].tolist()
            action = data["actions"]
            score = data["scores"]
            writer.writerow([game_uuid, deck, action, score])
    db.insert(directory)
    print(game_uuid)

# Insert the agent types that played this game into the database
save_agents()

# Play a game.
game.play_game()

# The game is over, save the states of the game into the database.
process_state_data()

# Put a debug point here to inspect the game object.
#input()
