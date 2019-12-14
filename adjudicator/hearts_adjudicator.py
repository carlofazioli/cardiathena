from base import *
from adjudicator.state import *


class HeartsAdjudicator(Adjudicator):
    # if the variable name is in all caps, it's a constant.
    # don't change it
    START_OF_ROUND = -2
    EXCHANGE_CARDS = -1
    # for additional tricks, just add 1
    FIRST_TRICK = 0
    LAST_TRICK = 12
    CALCULATE_ROUND_WINNER = 13
    # non-constants
    # list of agents
    trick_number = START_OF_ROUND
    trick_winner = -1
    CLOCKWISE = 0
    COUNTER_CLOCKWISE = 1
    ACROSS = 2
    NONE = 3
    pass_type = 0
    points = [0, 0, 0, 0]
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
        # need to get our players
        self.trick_number = self.START_OF_ROUND
        self.trick_winner = -1
        self.pass_type = self.CLOCKWISE
        self.points = [0, 0, 0, 0]
        # Hearts objects already initialize to the starting position.
        self.state = HeartsState()
        self.deal_cards()
        return self.state

    def step_game(self,
                  action: HeartsState):
        """
        Given an action by the agent whose turn it is, step_game() updates the state according to the rules and
        returns the new state.
        :param action: the Action of the Agent whose turn it is
        :return: the updated State
        """


    def get_state(self):
        """
        Tic-tac-toe is perfect-information so no masking takes place.
        :return: the current state
        """
        return self.state

    def is_finished(self):
        """
        The is_finished() method is a helper function to determine when the game is over.
        :return: boolean determination of whether the game is finished or not
        """

    def agent_turn(self):
        """
        The agent_turn() method is a helper function to determine from the current state whose turn it is and whether
        any elements of the current state need to be masked before showing the agent.
        :return:
        """
        # This code is kinda bad, its kinda broken
        # a note: looks like state.values contains which players all of the cards have been dealt out to
        while self.trick_number != self.FIRST_TRICK:
            #
            if self.trick_number == self.START_OF_ROUND:
                self.state.shuffle()
                self.trick_number = self.EXCHANGE_CARDS
            elif self.trick_number == self.EXCHANGE_CARDS:
                # exchange the cards between the players

                self.trick_number = self.FIRST_TRICK
            elif self.trick_number >= self.FIRST_TRICK:
                # do whatever we do for each trick

                self.trick_number += 1
            elif self.trick_number == self.CALCULATE_ROUND_WINNER:
                # do whatever we do when we finish a round
                self.trick_number = self.START_OF_ROUND
