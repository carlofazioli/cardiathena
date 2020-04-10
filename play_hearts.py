import csv
import uuid
import random
from datetime import datetime
from adjudicator.hearts_adjudicator import HeartsAdjudicator
from adjudicator.state import HeartsState
from agent.LowLayer import LowLayer
from agent.RandomHeartsAgent import RandomHeartsAgent
from agent.Equalizer import EqualizerAgent
from agent.Shooter import Shooter
from base import GameManager
from database.mysql.hearts import HeartsMySQLDatabase as db
from database.mysql.hearts.HeartsMySQLVariables import INSERT_GAME, CSV_DIR, MYSQL_SERVER

agents = ["RandomHeartsAgent", "LowLayer", "EqualizerAgent", "Shooter"]

def get_agent():
    """ 
    This function generates a random number in the range of the agents list and uses the string to make a new agent object to return.
    
    """

    agent_type = random.randint(0, (len(agents) - 1))

    try:
        agent = globals()[agents[agent_type]]()
    except KeyError:
        print("String not working: " + agents[agent_type])

    return agent


# Create the players, the adjudicator, and the game object.
game_uuid = uuid.uuid4().hex
adj = HeartsAdjudicator()
state = HeartsState()
agent_1 = get_agent()
agent_2 = get_agent()
agent_3 = get_agent()
agent_4 = get_agent()
agent_list = [0, agent_1, agent_2, agent_3, agent_4]
game = GameManager(agent_list,
                   adjudicator=adj,
                   state=state)


def save_game():
    """
    The save_game() method saves information about the game before it starts. Information that is saved includes the game
    uuid to uniquely identify each game, the date and time a game starts, agent_types that will participate in the game.

    """
    time_stamp = datetime.now()
    id_list = list()
    agent_set = list(set(agent_list))

    # Gets the id of each agent type ie The Random Agent's id is 1 and appends to a list
    for agent in agent_list:
        if agent is not 0:
            id = agent.__dict__.get("id")
            id_list.append(id)


    # Values is the data that will be saved
    values = (None, time_stamp, id_list[0], id_list[1], id_list[2], id_list[3], game_uuid)

    # Save the game table data into csv
    file_game_table = CSV_DIR + "{}_gametable.csv".format(game_uuid)
    with open(file_game_table, 'w') as file1:
        writer = csv.writer(file1, lineterminator='\n',)
        writer.writerow(["time_stamp", "agent1", "agent2", "agent3", "agent4"])
        writer.writerow([time_stamp, id_list[0], id_list[1], id_list[2], id_list[3]])

    # Save the agent table data into csv
    file_agent_table = CSV_DIR + "{}_agenttable.csv".format(game_uuid)
    with open(file_agent_table, 'w') as file2:
        writer = csv.writer(file2, lineterminator='\n',)
        writer.writerow(["id", "agent_type", "version"])
        for agent in agent_set:
            writer.writerow([agent.__dict__.get("id"), agent.__dict__.get("agent_type"), agent.__dict__.get("version")])

    if MYSQL_SERVER:
        # Insert the game data into the database
        db.query_database(INSERT_GAME, values)


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
    directory = CSV_DIR + "{}_statetable.csv".format(game_uuid)
    with open(directory, 'w') as file:
        writer = csv.writer(file, lineterminator='\n', )
        writer.writerow(["deck", "action", "score", "game_uuid"])
        for data in state_data:
            deck = data["deck"].tolist()
            action = data["actions"]
            score = data["scores"]
            writer.writerow([deck, action, score, game_uuid])
    if MYSQL_SERVER:
        db.insert_state(directory)


if MYSQL_SERVER:
    # Save starting game information
    save_game()
    # Play a game.
    game.play_game()
    # The game is over, save the states of the game into the database.
    process_state_data()

else:
    game.play_game()
