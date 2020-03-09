import random

from adjudicator.hearts_adjudicator import HeartsAdjudicator
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


class EqualizerAgent(Agent):
    """
    An random agent who selects from available legal moves.
    """

    def __init__(self):
        self.own_adj = HeartsAdjudicator()
        # Given the masked state, only cards in hand of agent
        # and played cards is available
        self.cards_in_hand = []

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """

        # print("partial_state.values: " + str(partial_state.values))
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                self.cards_in_hand.append(i)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            c1 = random.choice(self.cards_in_hand)
            self.cards_in_hand.remove(c1)
            c2 = random.choice(self.cards_in_hand)
            self.cards_in_hand.remove(c2)
            c3 = random.choice(self.cards_in_hand)
            self.cards_in_hand.remove(c3)
            three_cards = [c1, c2, c3]
            return HeartsAction(three_cards)

        # Agent picks a card to play
        # elif partial_state.trick_number > 0 and len(cards_in_hand) > 0:
        else:
            choice = self.select_card(partial_state)
            # print("minimizing agent is leading: " + str(self.is_lead(partial_state)))
            # print("minimizing agent is not void: " + str(self.not_void(partial_state)))
            self.cards_in_hand = []
            return HeartsAction(choice)

    def is_lead(self,
                partial_state: HeartsState):
        """Returns true if agent is leading currently"""
        played = partial_state.values[partial_state.values > 20]

        if len(played) >= 4:
            return True
        return False

    def select_card(self,
                    partial_state: HeartsState):
        # our player is leading, choosing a random card for now
        if self.is_lead(partial_state):

            # focus initially on voiding diamonds when leading
            choice = self.void_out_suits(partial_state)

        else:
            # we're following, not leading
            # todo random choice for now
            choice = random.choice(self.cards_in_hand)
        return choice

    def void_out_suits(self,
                       partial_state: HeartsState):
        # start by sorting out all of the clubs
        suits = self.sort_suits(partial_state)
        # the suit that we wish to pick a card from
        suit_to_void = []

        # todo right now leading is for when hearts has not been broken. may need to change strategy in future
        if len(suits[1]) != 0 or len(suits[0]) != 0:
            # neither diamonds or clubs have been voided, lead from one of these
            if len(suits[1]) > len(suits[0]):
                # we want to void clubs first
                suit_to_void = suits[0]
            else:
                # we want to void diamonds first
                suit_to_void = suits[1]
        else:
            # clubs and diamonds are both void, lead with spades or hearts
            if len(suits[3]) != 0:
                # leading with hearts if we can
                suit_to_void = suits[3]
            else:
                # no choice but to lead with spades
                suit_to_void = suits[2]

        # we now have our suit to pick a card from, want to lead with a low card
        choice = self.get_low_card(suit_to_void)
        return choice

    def sort_suits(self,
                   partial_state: HeartsState):
        """ Sort out the Cards by Suit and return a List of the suits"""
        # Clubs - diamonds - Spades - Hearts
        cards = []
        clubs = []
        diamonds = []
        spades = []
        hearts = []
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                cards.append(i)

        for i in range(4):
            start = i * 13
            end = start + 13
            for card in cards:
                if i == 0:
                    if start <= card < end:
                        clubs.append(card)
                elif i == 1:
                    if start <= card < end:
                        diamonds.append(card)
                elif i == 2:
                    if start <= card < end:
                        spades.append(card)
                elif i == 3:
                    if start <= card < end:
                        hearts.append(card)

        suits = [clubs, diamonds, spades, hearts]
        return suits

    def get_low_card(self,
                     suit_to_choose_from: list):
        # want to pick the lowest card from this suit
        suit_to_choose_from.sort()
        choice = suit_to_choose_from[0]
        return choice
