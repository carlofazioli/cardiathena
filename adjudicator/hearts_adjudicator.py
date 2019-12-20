from base import *
from adjudicator.state import HeartsState
from agent.RandomHeartsAgent import HeartsAction
import copy


class HeartsAdjudicator(Adjudicator):

    """
    The Adjudicator is an encapsulation of the rules.  It tracks the ground truth state of a game in progress,
    updating when presented with agent actions.

    state: an instance of State data type representing the state of the game.
    """

    def __init__(self):
        super().__init__()
        # The win conditions are the row-, column-, and diagonal-indices that make a tic tac toe.
        self.lead_suit = -2 #a variable that will range from 0-3 to determine the leading suit; -2 for beginning of round after pass; -1 for rest of trick starts
        self.pass_actions = []
        self.agent_types = []

    def start_game(self):
        """
        The start_game() method creates a new State data type instance and manipulates it to represent the starting
        point for the game.
        :return: State instance
        """
        # Hearts objects already initialize to the starting position.
        self.state = HeartsState()

        # Pass cards

        return self.state

    def step_game(self,
                  action: HeartsAction):
        """
        Given an action by the agent whose turn it is, step_game() updates the state according to the rules and
        returns the new state.
        :param action: the Action of the Agent whose turn it is
        :return: the updated State
        """
        # Check if game is finished
        if self.is_finished():
            return self.state
        else:
            # First trick of a round - all four players choose their cards before incrementing
            if self.state.trick_number == 0 and self.lead_suit == -2:
                # Implement pass here
                self.pass_actions.append(action.card_index)
                player_to_pass = 0
                # Pass 3 cards Clockwise(CW) : 1,2,3,4...
                if self.state.pass_type == 0:
                    player_to_pass = self.state.current_player + 1
                    # Loop around
                    if player_to_pass >= 5:
                        player_to_pass = 1

                # Pass 3 cards Counter-Clockwise(CCW) : 1,4,3,2...
                if self.state.pass_type == 1:
                    player_to_pass = self.state.current_player - 1
                    # Loop around
                    if player_to_pass <= 0:
                        player_to_pass = 1

                # Pass 3 cards Straight : 1 <-> 3 and 2 <-> 4
                if self.state.pass_type == 2:
                    player_to_pass = self.state.current_player + 2
                    # Loop around
                    if player_to_pass >= 3:
                        player_to_pass = self.state.current_player - 2

                # Pass cards to player_to_pass
                for card_i in self.pass_actions[len(self.pass_actions) - 1]:
                    self.state.values[card_i] = player_to_pass

                # Set next player to pass three cards
                self.state.current_player = self.state.current_player + 1

                # All players have passed cards
                if len(self.pass_actions) > 3:
                    # prepare found agent to handle two of clubs at beginning of round
                    self.state.trick_number = 1
                    self.state.pass_type += 1
                    self.lead_suit = -2
                    self.state.current_player = self.state.values[0]
                    if self.state.pass_type > 2:
                        self.state.pass_type = 0

            elif self.state.trick_number >= 1:
                # Add agent action to cards of tricks
                self.state.cards_of_trick.append(action.card_index)
                # Update state with encoding for played in current trick
                self.state.values[action.card_index] = (20 + self.state.values[action.card_index])

                # Check the current state for when trick is over
                if self.is_trick_over():

                    # the points accumulated for the current trick
                    trick_points = 0

                    # Find max card and then find the owner of the card
                    max_card = self.find_max_card()
                    trick_winner = self.state.values[max_card] - 20
                    self.state.trick_winner = trick_winner

                    print("trick winner:", trick_winner, " trick#:", self.state.trick_number, "  High card: ",
                          max_card)

                    # Check for point cards (Queen of Spades and Hearts)
                    for i in self.state.cards_of_trick:
                        # 36 is the index of the Queen of spades
                        if i == 36:
                            trick_points = trick_points + 13
                        # 39 and up are the indices for hearts
                        if i >= 39:
                            trick_points = trick_points + 1

                    # Update state points
                    self.state.points[trick_winner - 1] = self.state.points[trick_winner - 1] + trick_points

                    # All of these cards belong to the trick winner (tricks won)
                    for card in self.state.cards_of_trick:
                        self.state.values[card] = trick_winner + 10

                    # Clear out the cards in current trick
                    self.state.cards_of_trick.clear()
                    self.state.trick_number += 1

                    # Trick winner should be set up to start next trick
                    self.state.current_player = self.state.trick_winner

                    # suit is no longer leading at end of a trick
                    self.lead_suit = -1

                    # Check if new round, reset trick_number and deal new cards
                    if self.state.trick_number > 13:
                        # New round, shuffle cards, and Pass cards
                        self.state.trick_number = 0
                        self.state.trick_winner = 0
                        self.pass_actions.clear()
                        self.lead_suit = -2
                        self.state.shuffle()
                        for i in range(len(self.state.score)):
                            self.state.score[i] += self.state.points[i]
                            self.state.points[i] = 0
                else:
                    # Normal trickplay
                    self.state.current_player = self.state.current_player + 1
                    if self.state.current_player == 5:
                        self.state.current_player = 1
                    
                    # First card of trick has been played, remember the suit to make players follow it
                    if self.lead_suit == -1 or self.lead_suit == -2:
                        self.lead_suit = int(action.card_index / 13)

                    max_card = self.find_max_card()
                    trick_winner = self.state.values[max_card] - 20
                    self.state.trick_winner = trick_winner

        return self.state

    def get_state(self):
        """
        Tic-tac-toe is perfect-information so no masking takes place.
        :return: the current state
        """
        return self.state

    def is_finished(self):
        """
        The is_finished() method is a helper function to determine when the game is over.
        The game is over when the first player has reached 100 or more points
        :return: boolean determination of whether the game is finished or not
        """

        for i in range(0, 4):
            if self.state.score[i] >= 100:
                print("P1: ", self.state.score[0],
                      " P2: ", self.state.score[1],
                      " P3: ", self.state.score[2],
                      " P4: ", self.state.score[3])
                return True
        return False

    def agent_turn(self):
        """
        The agent_turn() method is a helper function to determine from the current state whose turn it is and whether
        any elements of the current state need to be masked before showing the agent.
        :return: player index and a masked state
        """
        # copy of the state to manipulate for the agent
        encode_state = copy.deepcopy(self.state)

        # Mask only cards that belong to agent for passing
        if encode_state.trick_number == 0 and self.lead_suit == -2:
            encode_state.hide_encoding(encode_state.current_player)
            return encode_state.current_player, encode_state

        # Make the two of clubs the only valid card if starting a round
        if encode_state.trick_number == 1 and self.lead_suit == -2:
            encode_state.values = encode_state.hide_encoding(encode_state.current_player)
            for i in range(len(encode_state.values)):
                if i != 0:
                    if encode_state.values[i] < 5:
                        # Turn values negative if they are held cards but not valid to play
                        encode_state.values[i] = encode_state.values[i]*(-1)
            return encode_state.current_player, encode_state

        # Player can play any of their cards if they lead the trick (unless starting a round)
        if self.lead_suit == -1:
            # Need to code in that players can not lead with any Hearts cards until that suit has been "broken"
            encode_state.values = encode_state.hide_encoding(encode_state.current_player)
            return encode_state.current_player, encode_state
        
        # first hides values then changes returned ones if they can not be seen
        encode_state.values = encode_state.hide_encoding(encode_state.current_player)
        # beginning of range of valid cards
        begin = 13 * self.lead_suit
        # end of range of valid cards
        end = 13 * (self.lead_suit + 1)
        
        # Check that the player actually has cards in the current suit before hiding everything else
        has_suit = False
        for i in range(begin, end):
            if 0 < encode_state.values[i] < 5:
                has_suit = True
        if has_suit == False:
            # Player did not have suit and can play whatever
            return encode_state.current_player, encode_state
        # Encode it if we know they have valid cards
        for i in range(len(encode_state.values)):
            if i < begin or i >= end:
                if encode_state.values[i] < 5:
                    encode_state.values[i] = encode_state.values[i]*(-1)
        return encode_state.current_player, encode_state

    def hearts_broken(self):
        if len(list(x for x in self.state.values if 39 <= x <= 51)) > 10:
            return True
        return False

    def is_trick_over(self):
        if len(list(x for x in self.state.values if 21 <= x <= 24)) >= 4:
            return True
        return False

    def find_max_card(self):
        begin = 13 * self.lead_suit  # beginning of range of valid cards
        end = 13 * (self.lead_suit + 1)  # end of range of valid cards

        card_max = 0

        if begin < 0 and end < 0:
            card_max = self.state.cards_of_trick[0]
        else:
            for x in self.state.cards_of_trick:
                if begin <= x < end:
                    if x > card_max:
                        card_max = x
        return card_max
