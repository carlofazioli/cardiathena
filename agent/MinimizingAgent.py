import random

import numpy as np

from adjudicator import hearts_adjudicator
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


class MinimizingAgent(Agent):
    """
    An random agent who selects from available legal moves.
    """

    def __init__(self):
        self.own_adj = HeartsAdjudicator()
        self.cards_in_hand = []

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """
        # Given the masked state, only cards in hand of agent is available
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                self.cards_in_hand.append(i)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
           # self.pick_trouble_card(partial_state)
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
            choice = random.choice(self.cards_in_hand)
            player_number = self.own_adj.current_player(partial_state)
            trick_w = self.own_adj.trick_leader(partial_state)
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

    def not_void(self,
                 partial_state: HeartsState):
        lead_suit = self.own_adj.lead_suit(partial_state)
        begin = 13 * lead_suit  # beginning of range of valid cards
        end = 13 * (lead_suit + 1)  # end of range of valid cards
        for x in self.cards_in_hand:
            if begin <= x < end:
                return True
        return False

    """    Pass highest cards in trouble suits: suits where 
    the lowest card is higher than any other lowest card in
     other suits. If the player becomes void, then pass off 
     the next high cards from the next trouble suit. 
    """

    def pick_trouble_card(self, partial_state: HeartsState):

        """Choose the suit with the least amount of cards
            and pass those starting with the highest card"""
        trouble = []
        suits = self.sort_suits(partial_state)
        num_cards = -1
        for s in suits:
            if len(s) > num_cards:
                num_cards = len(s)
                trouble = s

    def sort_suits(self,
                   partial_state: HeartsState):
        cards = []
        clubs = []
        Diamond = []
        spades = []
        hearts = []
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                cards.append(i)

            """ Sort out the Cards by Suit """
            # Clubs - Diamond - Spades - Hearts
            for i in range(4):
                start = i * 13
                end = start + 13
                for card in cards:
                    # print("I : "+str(i)+"  Card "+str(card))
                    if i == 0:
                        # print("Club Enter")
                        if start <= card < end:
                            clubs.append(card)
                        #   print("Club Added")
                    elif i == 1:
                        # print("Diamond Enter")
                        if start <= card < end:
                            Diamond.append(card)
                        #  print("Diamond Added")
                    elif i == 2:
                        # print("Spade Enter")
                        if start <= card < end:
                            spades.append(card)
                        #    print("Spade Added")
                    elif i == 3:
                        #  print("Hearts Enter")
                        if start <= card < end:
                            hearts.append(card)
                        #   print("Hearts Added")

                suits = [clubs, Diamond, spades, hearts]
                return suits
