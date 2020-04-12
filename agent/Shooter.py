import random
import numpy as np
import math
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



class Shooter(Agent):
    """
    An agent who attempts to shoot for the moon.
    """

    def __init__(self):
        self.own_adj = HeartsAdjudicator()
        self.cards_in_hand = []
        self.id = 4
        self.agent_name = "The Shooter"
        self.version = 1.0

    def __repr__(self):
        return {"id": self.id, "name": self.agent_name, "version": self.version}

    def __str__(self):
        return self.agent_name

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """
        # Given the masked state, only cards in hand of agent is available
        self.cards_in_hand = []

        for i in range(len(partial_state.deck)):
            if 0 < partial_state.deck[i] < 5:
                self.cards_in_hand.append(i)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            three_cards = []
            hearts = self.get_hearts(self.cards_in_hand)
            lowest_heart = self.get_lowest(hearts)
            while (len(lowest_heart) > 0 and len(three_cards) < 3):
                # We can only play a heart when we have a heart
                # First we get the lowest heart and the lowest card
                chosen_heart = lowest_heart[0]
                heart_value = chosen_heart % 13
                lowest = random.choice(self.get_lowest(self.cards_in_hand))
                lowest_value = lowest % 13
                # We know lowest heart can not be lower than lowest card so we do not have to check that
                if (chosen_heart == lowest):
                    # The lowest card is a heart
                    three_cards.append(chosen_heart)
                    # Remove from lists so it does not get chosen again
                    hearts.remove(chosen_heart)
                    self.cards_in_hand.remove(chosen_heart)
                    # Find our next lowest cards to pass on
                    lowest_heart = self.get_lowest(hearts)
                elif ((lowest_value - 2) <= heart_value <= (lowest_value + 2)):
                    # Heart is slightly higher than lowest but play it anyways
                    three_cards.append(chosen_heart)
                    # Remove from lists so it does not get chosen again
                    hearts.remove(chosen_heart)
                    self.cards_in_hand.remove(chosen_heart)
                    # Find our next lowest cards to pass on
                    lowest_heart = self.get_lowest(hearts)
                else:
                    # Should only be in here if lowest card is significantly lower than lowest heart
                    three_cards.append(lowest)
                    # Only remove from cards in hand since it is not a heart
                    self.cards_in_hand.remove(lowest)
            # We either have all three cards as hearts cards or we need more
            while (len(three_cards) < 3):
                lowest = random.choice(self.get_lowest(self.cards_in_hand))
                three_cards.append(lowest)
                self.cards_in_hand.remove(lowest)
            return HeartsAction(three_cards)

        # Agent picks a card to play
        #elif partial_state.trick_number > 0 and len(cards_in_hand) > 0:
        else:
            # choice = random.choice(cards_in_hand)
            choice = self.select_card(partial_state)
            return HeartsAction(choice)

    def select_card(self,
                    partial_state: HeartsState):
        if self.is_lead(partial_state):
            # We are leading the trick
            if self.is_early(partial_state):
                # Early in the game so get rid of cards that will make it hard to take points
                lowest = self.get_lowest(self.cards_in_hand)
                return random.choice(lowest)
            else:
                # Later in the game so attempt to take the points
                highest = self.get_highest(self.cards_in_hand)
                return random.choice(highest)
        else:
            # We are following a trick
            if self.is_early(partial_state):
                lowest = self.get_lowest(self.cards_in_hand)
                return random.choice(lowest)
            else:
                # Later in the game so try to take tricks from players
                # if we are capable of taking the trick
                if (self.is_last(partial_state)):
                    # We know the trick is over after this action so do the bare minimum to win
                    if self.following_lead(partial_state, self.cards_in_hand):
                        # We can follow suit so take it
                        lowest_high = self.lowest_high(partial_state, self.cards_in_hand)
                        return random.choice(lowest_high)
                    else:
                        # We could not follow suit so do not bother trying to win
                        lowest = self.get_lowest(self.cards_in_hand)
                        return random.choice(lowest)
                else:
                    # Not last so be safe and play highest
                    if self.following_lead(partial_state, self.cards_in_hand):
                        # We could possibly take it so try to
                        highest = self.get_highest(self.cards_in_hand)
                        return random.choice(highest)
                    else:
                        # We can not follow so there is no chance of taking it
                        lowest = self.get_lowest(self.cards_in_hand)
                        return random.choice(lowest)

    def is_lead(self,
                partial_state: HeartsState):
        """Returns true if agent is leading currently"""
        played = partial_state.deck[partial_state.deck > 20]

        if len(played) >= 4:
            return True
        return False

    def is_early(self,
                 partial_state: HeartsState):
        """Returns true if it is still early in the game.
        Check if points have been broken. If they have not, check if half the deck remains."""
        if (self.points_broken(partial_state)):
            # Points have been broken so it is no longer early in the game
            return False
        if (len(partial_state.deck[partial_state.deck > 10]) < 52/2):
            # A deck starts with 52 cards
            # We are in the early half of the game if less than half the cards have been played
            return True
        # We are in the later half of the game if more than half the cards are remaining
        return False

    def is_last(self,
                partial_state: HeartsState):
        """Returns true if the player is the last to play in a trick."""
        if (len(partial_state.deck[partial_state.deck > 20]) == 3):
            # Four players so this player is last when the other three have played
            return True
        return False

    def get_lowest(self,
                   cards: list):
        """Finds a list of cards with the lowest value in the players hand. If this function
        returns more than one card of the same value from different suits, the player will
        make their choice once they receive the list."""
        # Start a list with the first card
        lowest = []
        for i in cards:
            if (lowest == [] or (i % 13) == (lowest[0] % 13)):
                # Append the first card in hand if empty or append card of same value
                lowest.append(i)
            elif ((i % 13) < (lowest[0] % 13)):
                # A smaller value was found so restart the list
                lowest = [i]
        # Return the list of lowest cards once the hand has been looped through
        return lowest

    def get_highest(self,
                    cards: list):
        """Similar to get_lowest(partial_state) except it finds the highest cards"""
        highest = []
        for i in cards:
            if (highest == [] or (i % 13) == (highest[0] % 13)):
                # Append the first card in hand if empty or append card of same value
                highest.append(i)
            elif ((i % 13) > (highest[0] % 13)):
                # A bigger value was found so restart the list
                highest = [i]
        # Return the list of highest cards once the hand has been looped through
        return highest

    def lowest_high(self,
                    partial_state: HeartsState,
                    cards: list):
        """Find a card that is high enough to take the current trick but is as low as can be
        so as to save higher cards for later tricks"""
        # Find the highest card of the cards that are in play
        highest_down = self.get_highest(np.where(partial_state.deck > 20)[0])
        # Search for lowest high card by comparing to currently highest card
        lowest_high = []
        for i in cards:
            if ((i % 13) > (highest_down[0] % 13)):
                # Current card is higher than the currently placed card
                if (lowest_high == [] or (i % 13) < (lowest_high[0] % 13)):
                    # List is empty or we found a lower high card so we start the list
                    lowest_high = [i]
                elif ((i % 13) == (lowest_high[0] % 13)):
                    # Check for equally high cards
                    lowest_high.append(i)
        if (len(lowest_high) > 0):
            # Check to see if any cards that are high enough were found
            return lowest_high
        # Only here when the player is not capable of taking the trick so go with lowest card
        return self.get_lowest(cards)

    def get_hearts(self,
                   cards : list):
        """Takes a list of cards and returns a list that only holds hearts cards"""
        hearts = []
        for i in cards:
            if (38 < i <52):
                hearts.append(i)
        return hearts

    def points_broken(self,
                      partial_state: HeartsState):
        """Check to see if points have been broken."""
        played_cards = np.where(partial_state.deck >= 10)[0]
        # Get the hearts cards (the where does not really matter, we just need a count of them)
        points = np.where(played_cards > 38)[0]
        if (len(points) > 0):
            # At least one heart has been played so points are broken
            return True
        # Check if the queen of spades has been played
        points = np.where(played_cards == 36)[0]
        if (len(points) > 0):
            # The queen was played
            return True
        # None of the points cards have been played
        return False

    def following_lead(self,
                       partial_state: HeartsState,
                       cards: list):
        """Check if the player is capable of following suit before trying to take the trick.
        Receives the partial state and a list representing the players hand."""
        # Find the leading card to figure out its suit
        lead = np.where(partial_state.deck >= 30)[0][0]
        # Divide by 13 to find the suit type
        if (math.floor((cards[0]/13)) == math.floor((lead/13))):
            # Player has to follow if they have a card that is the same suit as the leader
            return True
        # Player can not follow the trick leader
        return False