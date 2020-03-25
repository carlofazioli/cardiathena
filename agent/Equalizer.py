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
        self.id = 3
        self.agent_name = "The Equalizer"
        self.version = 1.0

    def __repr__(self):
        return {"id": self.id, "name": self.agent_name, "version": self.version}

    def __str__(self):
        return self.agent_name

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

    def passing(self, partial_state: HeartsState):
        """Want to void out first Clubs, Diamonds, Spades, and lastly Hearts"""
        hand = self.sort_suits(partial_state)
        # We want to void out Clubs - Diamonds - Spades - Hearts
        # priority = [ 0 , 1, 2 ,3 ]
        # Reference to all the amount of cards in each suit
        # suit_map = {
        #        "D":len(hand[1]),
        #        "C":len(hand[0]),
        #        "S":len(hand[2]),
        #        "H":len(hand[3])
        # }

        cards_to_pass = []
        suit_counter = 0
        # Follows the order of priority to void suits.
        for suit in hand:
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
        return cards_to_pass[0:3]

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
        """ This function selects the suit we want to try and void when leading, the idea is to start with voiding either Clubs
        or Diamonds (whichever is shortest) followed by Hearts and then Spades."""
        # start by sorting out all of the clubs
        suits = self.sort_suits(partial_state)
        # the suit that we wish to pick a card from
        suit_to_void = []

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

        # see if we're void in the suit we need to follow, we are void if we have 2 or more suits that are non-empty
        # inside of the suits list
        counter = 0
        for suit in suits:
            if len(suit) != 0:
                counter = counter + 1
                # only need this for the else portion, if counter == 1 then that means this agent isn't void, so using
                # this variable will work
                valid_suit = suit

        # redid the logic. if we're void in the suit we need to follow: we want to stick the queen on the trick
        # winner (if we have it) or play our highest hearts cards

        # if the counter is greater than 1, we are void in the trick leader's suit
        if counter > 1:
            # if we have the queen of spades, want to play it
            queen_index = self.have_queen(suits[2])
            if queen_index != 0:
                choice = queen_index
            # otherwise if we have hearts, we want to play our highest heart card (we're void so its safe to do)
            elif len(suits[3]) != 0:
                choice = self.get_highest_card(suits[3])
            # dont have queen of spades, don't have hearts, want to pick highest card from clubs, then diamonds.
            # Spades is the very last thing we want to play
            else:
                # have clubs, play the highest clubs card
                if len(suits[0]) != 0:
                    choice = self.get_highest_card(suits[0])
                # have diamonds, play the highest clubs card
                elif len(suits[1]) != 0:
                    choice = self.get_highest_card(suits[1])
                # have clubs, play the highest clubs card
                else:
                    choice = self.get_highest_card(suits[2])

        # else we're not void
        else:
            # pick the lowest card and go.
            choice = self.get_highest_safe_card(valid_suit, partial_state)

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

    def have_queen(self,
                   spades_suit: list):
        """ Get and return the Queen of Spades"""
        for card in spades_suit:
            if card == 36:
                # if we have the queen, return it
                return card
        # otherwise return 0
        return 0

    def played_cards_in_trick(self,
                              partial_state: HeartsState):
        """ Get the currently played cards in the trick"""
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

    def get_highest_card(self,
                         suit_to_choose_from: list):
        """In this function we want to want to pick the highest card from this suit"""
        suit_to_choose_from.sort()
        choice = suit_to_choose_from[-1]
        return choice

    def get_highest_safe_card(self,
                              suit_to_choose_from: list,
                              partial_state: HeartsState):
        """In this function we want to pick the safest high card from the suit we need to follow"""
        # want to pick the safest high card from the suit

        suit_to_choose_from.sort()
        # get the cards already played in this trick
        trick_cards = self.played_cards_in_trick(partial_state)
        hearts_played = 0
        queen_played = False
        for card in trick_cards:
            if card == 36:
                # if the queen has been played, we're going to want to choose the lowest card we can
                queen_played = True
            if 51 >= card >= 39:
                # if the queen has been played, we're going to want to choose the lowest card we can
                hearts_played = hearts_played + 1

        # may or may not want this as part of the if: partial_state.score[self.player_position - 1] >= 5:
        # if the queen has been played or a bunch of hearts have been played this round
        # or if this agent is playing directly after the leader (so we don't know what comes next)
        if queen_played or hearts_played >= 2 or len(trick_cards) <= 1:
            # play the lowest card
            choice = suit_to_choose_from[0]
        else:
            # the queen hasnt been played and we haven't racked up a bunch of points
            # so this agent is going to be risky and play its highest card (that isn't the queen)
            choice = suit_to_choose_from[-1]
            if choice == 36 and len(suit_to_choose_from) >= 2:
                # making sure we're not playing the queen of spades on ourselves...
                choice = suit_to_choose_from[-2]
        return choice

