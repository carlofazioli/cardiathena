import random
from agent.LowLayer import LowLayer
from base import GameManager
from adjudicator.hearts_adjudicator import HeartsAdjudicator
from adjudicator.state import HeartsState
from agent.RandomHeartsAgent import RandomHeartsAgent
from agent.Shooter import Shooter


# Create the players, the adjudicator, and the game object.
agent_1 = RandomHeartsAgent()
agent_2 = RandomHeartsAgent()
agent_3 = LowLayer()
agent_4 = Shooter()
adj = HeartsAdjudicator()
state = HeartsState()
game = GameManager(agent_list=[0, agent_1, agent_2, agent_3, agent_4],
                   adjudicator=adj,
                   state=state)

# Play a game.
game.play_game()
game.save_game()

# Put a debug point here to inspect the game object.
input()
