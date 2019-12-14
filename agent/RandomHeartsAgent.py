from adjudicator.hearts_adjudicator import *
import random


class HeartsAction(Action):
    """
    A tic-tac-toe action is a specification of a player adding a mark to a position
    """
    def __init__(self,
                 position: int):
        self.position = position


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
        # Parse the state for legal moves:
        # legal_indices = [i for (i, mark) in enumerate(partial_state.positions) if mark == 0]
        count = 0
        legal_indices = []
        for i in np.nditer(partial_state):
            if i != 0:
                legal_indices.append(count)
            count = count + 1
        choice = random.choice(legal_indices)
        return HeartsAction(choice)
