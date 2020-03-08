import random

import numpy as np

from adjudicator.state import HeartsState
from base import Action, Agent


class HeartsAction(Action):
    """
    A Hearts action is the card index chosen by the agent
    """
    def __init__(self,
                 card_index):
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
        # Given the masked state, only cards in hand of agent is available
        cards_in_hand = list()

        # Creates a list of the available cards that a player can play.
        for index, card in enumerate(partial_state.values):
            if 0 < card < 5:
                cards_in_hand.append(index)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            # Random sampling of the cards in hand without replacement.
            three_cards = random.sample(cards_in_hand,3)
            return HeartsAction(three_cards)

        # Agent picks a card to play
        #elif partial_state.trick_number > 0 and len(cards_in_hand) > 0:
        else:
            choice = random.choice(cards_in_hand)
            return HeartsAction(choice)
