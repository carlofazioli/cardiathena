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
    An agent who selects an action with the mindset of trying to inflict as many points as possible on the other players.
    """

    def __init__(self):
        self.own_adj = HeartsAdjudicator()
        # Given the masked state, only cards in hand of agent
        # and played cards is available
        self.cards_in_hand = []
        self.player_position = -1

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one that will allow it to
        inflict points on other players.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """

        # print("partial_state.values: " + str(partial_state.values))
        card_index = 0
        for i in partial_state.values:
            if 0 < i < 5:
                self.cards_in_hand.append(card_index)
                self.player_position = i
            card_index = card_index + 1

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            # c1 = random.choice(self.cards_in_hand)
            # self.cards_in_hand.remove(c1)
            # c2 = random.choice(self.cards_in_hand)
            # self.cards_in_hand.remove(c2)
            # c3 = random.choice(self.cards_in_hand)
            # self.cards_in_hand.remove(c3)
            # three_cards = [c1, c2, c3]

            three_cards = self.passing(partial_state)
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
        """The main selection routine for if the agent is leading or following a trick."""
        # our player is leading, choosing a random card for now
        if self.is_lead(partial_state):

            # focus initially on voiding diamonds when leading
            choice = self.void_out_suits(partial_state)

        else:
            # we're following, not leading
            # so the idea here is to follow with our highest card for this suit (unless we're Hearts/Spades
            choice = self.following_suit(partial_state)
        return choice

    def void_out_suits(self,
                       partial_state: HeartsState):
        """ This function selects the suit we want to try and void, the idea is to start with voiding either Clubs
        or Diamonds (whichever is shortest) followed by Hearts and then Spades."""
        # start by sorting out all of the clubs
        suits = self.sort_suits(partial_state)
        # the suit that we wish to pick a card from
        suit_to_void = []

        # todo right now leading is for when hearts has not been broken. may want to change strategy in future
        # note that this nested if-else block can handle both cases of whether the agent is:
        # - void in the suit the trick leader has
        # - able to follow suit
        if len(suits[1]) != 0 or len(suits[0]) != 0:
            # neither diamonds or clubs have been voided, lead from one of these
            if len(suits[1]) == 0 or len(suits[1]) > len(suits[0]) != 0:
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

    def following_suit(self,
                       partial_state: HeartsState):
        """ This function will still attempt to void Clubs or Diamonds if it can, it may also try and play
        the highest card in its suit, if it thinks it can afford to take on potential points."""
        # depending on the suit we want to follow in different ways
        suits = self.sort_suits(partial_state)

        # so my idea is that if the suit we're following with is Hearts or Spades
        # we will want to go with our lowest card
        if len(suits[2]) != 0 or len(suits[3]) != 0:
            # if we're void in the suit we're trying to follow, want to avoid playing spades
            # going to play and potentially break hearts if we can
            if len(suits[3]) != 0:
                if len(suits[3]) == 0:
                    print("hi-follow")
                choice = self.get_low_card(suits[3])
            else:
                if len(suits[2]) == 0:
                    print("hi-follow")
                choice = self.get_low_card(suits[2])
        else:
            # clubs or diamonds have been played, follow with our high card (if we can)
            # we care less here about which to pick if we're void, so just go with the suit
            # thats the smallest
            if len(suits[1]) == 0 or len(suits[1]) > len(suits[0]) != 0:
                choice = self.get_highest_safe_card(suits[0], partial_state)
            else:
                choice = self.get_highest_safe_card(suits[1], partial_state)
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
        card_index = 0
        for i in partial_state.values:
            if 0 < i < 5:
                cards.append(card_index)
            card_index = card_index + 1

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

    def played_cards_in_trick(self,
                              partial_state: HeartsState):
        """ Get the currently played cards in the trick"""
        # why
        trick_cards = []
        card_index = 0
        for i in partial_state.values:
            if 20 < i < 35:
                trick_cards.append(card_index)
            card_index = card_index + 1
        return trick_cards

    def get_low_card(self,
                     suit_to_choose_from: list):
        """In this function we want to want to pick the lowest card from this suit"""
        suit_to_choose_from.sort()
        choice = suit_to_choose_from[0]
        return choice
    def passing(self, partial_state: HeartsState):
        hand = self.sort_suits(partial_state)
        # We want to void out Clubs - Diamonds - Spades - Hearts
        pirority = [ 0 , 1, 2 ,3 ]
        # Reference to all the amount of cards in each suit
        suit_map = {
                "D":len(hand[1]),
                "C":len(hand[0]),
                "S":len(hand[2]),
                "H":len(hand[3])
        }

        cards_to_pass = []
        suit_counter = 0
        # Follows the order of priority to void suits.
        for  suit in hand:
            # Clubs first since they are the first suit played
            if len(suit) > 0 :
                suit.reverse()
                for card in suit:
                    # Avoid giving away the queen of spades
                    if (suit_counter != 2) & (card != 36):
                        cards_to_pass.append(card)
            if len(cards_to_pass) > 3:          # There is enough cards to pass
                break
            suit_counter += 1
            # rinse and repeat the first part but with other suits
        return  cards_to_pass[0:3]


    def get_highest_safe_card(self,
                              suit_to_choose_from: list,
                              partial_state: HeartsState):
        """In this function we want to pick the safest high card from the suit we need to follow"""
        # want to pick the safest high card from the suit

        suit_to_choose_from.sort()
        # get the cards already played in this trick
        trick_cards = self.played_cards_in_trick(partial_state)
        queen_played = False
        for card in trick_cards:
            if card == 36:
                # if the queen has been played, we're going to want to choose the lowest card we can
                queen_played = True
        # if the queen has been played or our points are over 10, this
        # agent is going to play the lowest card it can
        if queen_played or partial_state.points[self.player_position] >= 10:
            choice = suit_to_choose_from[0]
        else:
            # todo if our agent has the queen we may want some different behavior
            # the queen hasnt been played and we haven't racked up a bunch of points
            # so this agent is going to be risky and play its highest card (that isn't the queen)
            choice = suit_to_choose_from[-1]
            if choice == 36:
                # making sure we're not playing the queen of spades on ourselves...
                choice = suit_to_choose_from[-2]
        return choice
