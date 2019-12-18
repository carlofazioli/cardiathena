from base import *
from adjudicator.state import HeartsState
from agent.RandomHeartsAgent import HeartsAction


class HeartsAdjudicator(Adjudicator):

    """
    The Adjudicator is an encapsulation of the rules.  It tracks the ground truth state of a game in progress,
    updating when presented with agent actions.

    state: an instance of State data type representing the state of the game.
    """

    def __init__(self):
        super().__init__()
        # The win conditions are the row-, column-, and diagonal-indices that make a tic tac toe.

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
            # Add agent action to cards of tricks
            self.state.cards_of_trick.append(action.card_index)
            # Update state with encoding for played in current trick
            self.state.values[action.card_index] = (20 + self.state.current_player)

            # Check the current state for when trick is over
            if self.is_trick_over():

                # the points accumulated for the current trick
                trick_points = 0

                # The index of the max card in cards_of_trick is the player with the highest card for now
                max_card = (self.state.cards_of_trick.index(max(self.state.cards_of_trick)))
                self.state.trick_winner = max_card
                print("trick winner:", max_card, " trick#:", self.state.trick_number, "  High card: ",
                      self.state.cards_of_trick[max_card])
                # Check for point cards (Queen of Spades and Hearts)
                for i in self.state.cards_of_trick:
                    # 36 is the index of the Queen of spades
                    if i == 36:
                        trick_points = trick_points + 13
                    # 39 and up are the indices for hearts
                    if i >= 39:
                        trick_points = trick_points + 1

                # Update state score
                self.state.score[max_card] = self.state.score[max_card] + trick_points

                # All of these cards belong to the trick winner (tricks won)
                for card in self.state.cards_of_trick:
                    self.state.values[card] = max_card + 11

                # Clear out the cards in current trick
                self.state.cards_of_trick.clear()
                self.state.trick_number += 1

                # Check if new round, reset trick_number and deal new cards
                if self.state.trick_number > 12:
                    # New round, Get new state and Pass cards
                    self.state.trick_number = 0
                    self.state.trick_winner = -1
                    self.state.shuffle()
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
        player = self.state.current_player

        # Start of a new round, return the player with 2 of clubs
        if self.state.trick_winner == -1:
            self.state.current_player = self.state.values[0]
            player = self.state.current_player
            self.state.trick_winner = 0

        # Set next player
        elif not self.is_trick_over():
            player = player + 1
            if player == 5:
                player = 1
            self.state.current_player = player
        # Trick is over, current player is set to trick winner
        else:
            self.state.current_player = self.state.trick_winner

        return player, self.state.hide_encoding(player)

    def is_trick_over(self):
        if len(list(x for x in self.state.values if 21 <= x <= 24)) >= 4:
            return True
        return False
