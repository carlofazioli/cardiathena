import random
from adjudicator.hearts_adjudicator import *
from numpy import size


class HeartsAction(Action):
    """
    A Hearts action is the card index chosen by the agent
    """
    def __init__(self,
                 card_index: int):
        self.card_index = card_index

    def __str__(self):
        return str(self.card_index)


class RandomHeartsAgent(Agent):
    """
    An random agent who selects from available legal moves.
    """

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """
        # Get legal indices, given the masked state, the legal values will be between 1 and 4
        legal_indices = []
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                legal_indices.append(i)

        # Return element if only one choice available otherwise choose a random card
        if legal_indices:
            choice = random.choice(legal_indices)
            return HeartsAction(choice)
        else:
            return None
