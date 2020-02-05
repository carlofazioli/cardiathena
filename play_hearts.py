from base import GameManager
from adjudicator.hearts_adjudicator import HeartsAdjudicator
from agent.RandomHeartsAgent import RandomHeartsAgent
from database import mysql_example as mysql

# Create the players, the adjudicator, and the game object.
agent_1 = RandomHeartsAgent()
agent_2 = RandomHeartsAgent()
agent_3 = RandomHeartsAgent()
agent_4 = RandomHeartsAgent()
adj = HeartsAdjudicator()
game = GameManager(agent_list=[0, agent_1, agent_2, agent_3, agent_4],
                   adjudicator=adj)

#mysql.initialize_db()

# Play a game.
game.play_game()
game.save_game()

