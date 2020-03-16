import random
import numpy as np
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
    
    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """
        # Given the masked state, only cards in hand of agent is available
        self.cards_in_hand = []

        #print("partial_state.values: " + str(partial_state.values))
        for i in range(len(partial_state.values)):
            if 0 < partial_state.values[i] < 5:
                self.cards_in_hand.append(i)

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            three_cards = []
            hearts = self.get_hearts(self.cards_in_hand)
            lowest_heart = self.get_lowest(hearts)
            while (len(lowest_heart) > 0 and len(three_cards) < 3):
                # We can only play a heart when we have a heart
                chosen_card = random.choice(lowest_heart)
                three_cards.append(chosen_card)
                # Remove from lists so it does not get chosen again
                hearts.remove(chosen_card)
                self.cards_in_hand.remove(chosen_card)
                # Find our next lowest cards to pass on
                lowest_heart = self.get_lowest(hearts)
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
                # TODO is_early most likely counts too much time when it comes to whether
                # we should follow with low cards or not so we can update it later
                lowest = self.get_lowest(self.cards_in_hand)
                return random.choice(lowest)
            else:
                # Later in the game so try to take tricks from players
                # TODO we should be checking if we can even follow suit to know
                # if we are capable of taking the trick
                if (self.is_last):
                    # We know the trick is over after this action so do the bare minimum to win
                    lowest_high = self.lowest_high(partial_state, self.cards_in_hand)
                    return random.choice(lowest_high)
                else:
                    # Not last so be safe and play highest
                    highest = self.get_highest(self.cards_in_hand)
                    return random.choice(highest)
            return random.choice(self.cards_in_hand)

    def is_lead(self,
                partial_state: HeartsState):
        """Returns true if agent is leading currently"""
        played = partial_state.values[partial_state.values > 20]

        if len(played) >= 4:
            return True
        return False

    def is_early(self,
                 partial_state: HeartsState):
        """Returns true if it is still early in the game.
        Start with the basic strategy of checking if half the hand remains"""
        if (len(partial_state.values[partial_state.values > 10]) < 52/2):
            # A deck starts with 52 cards
            # We are in the early half of the game if less than half the cards have been played
            return True
        # We are in the later half of the game if more than half the cards are remaining
        return False

    def is_last(self,
                partial_state: HeartsState):
        """Returns true if the player is the last to play in a trick."""
        if (len(partial_state.values[partial_state.values > 20]) == 3):
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
        # TODO This is currently finding the highest card rather than
        # highest card following suit.
        highest_down = self.get_highest(np.where(partial_state.values > 20)[0])
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