import random

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
        cards_in_hand = []
        #print("partial_state.values: " + str(partial_state.values))
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                cards_in_hand.append(i)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            c1 = random.choice(cards_in_hand)
            cards_in_hand.remove(c1)
            c2 = random.choice(cards_in_hand)
            cards_in_hand.remove(c2)
            c3 = random.choice(cards_in_hand)
            cards_in_hand.remove(c3)
            three_cards = [c1, c2, c3]
            return HeartsAction(three_cards)

        # Agent picks a card to play
        #elif partial_state.trick_number > 0 and len(cards_in_hand) > 0:
        else:
            choice = random.choice(cards_in_hand)
            return HeartsAction(choice)
