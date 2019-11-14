from base import *
import random


class TicTacToeState(State):
    """
    A tic-tac-toe state can be represented by a vector indicating the player mark in each position.

    Position indices:
    0 | 1 | 2
    ---------
    3 | 4 | 5
    ---------
    6 | 7 | 8

    Player mark encodings:
        0: empty
        1: player 1
        2: player 2
    """
    def __init__(self):
        self.positions = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.scores = [0, 0]


class TicTacToeAction(Action):
    """
    A tic-tac-toe action is a specification of a player adding a mark to a position
    """
    def __init__(self,
                 position: int):
        self.position = position


class RandomTicTacToeAgent(Agent):
    """
    An random agent who selects from available legal moves.
    """

    def get_action(self,
                   partial_state: TicTacToeState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """
        # Parse the state for legal moves:
        legal_indices = [i for (i, mark) in enumerate(partial_state.positions) if mark == 0]
        choice = random.choice(legal_indices)
        return TicTacToeAction(choice)


class TicTacToeAdjudicator(Adjudicator):
    """
    The Adjudicator is an encapsulation of the rules.  It tracks the ground truth state of a game in progress,
    updating when presented with agent actions.

    state: an instance of State data type representing the state of the game.
    """
    def __init__(self):
        super().__init__()
        # The win conditions are the row-, column-, and diagonal-indices that make a tic tac toe.
        self.win_conditions = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]

    def start_game(self):
        """
        The start_game() method creates a new State data type instance and manipulates it to represent the starting
        point for the game.
        :return: State instance
        """
        # TicTacToeState objects already initialize to the starting position.
        self.state = TicTacToeState()
        return self.state

    def step_game(self,
                  action: TicTacToeAction):
        """
        Given an action by the agent whose turn it is, step_game() updates the state according to the rules and
        returns the new state.
        :param action: the Action of the Agent whose turn it is
        :return: the updated State
        """
        count_ones = self.state.positions.count(1)
        count_twos = self.state.positions.count(2)
        if count_ones == count_twos:
            # It's agent 1's turn:
            mark = 1
        else:
            # It's agent 2's turn:
            mark = 2
        self.state.positions[action.position] = mark
        # If the game is finished, updated the score.
        if self.is_finished():
            # Check if a win condition is satisfied.
            win_condition = False
            for condition in self.win_conditions:
                marks = [self.state.positions[i] for i in condition]
                if marks.count(1) == 3:
                    # Player 1 has won:
                    self.state.scores = [1, 0]
                    win_condition = True
                elif marks.count(2) == 3:
                    # Player 2 has won:
                    self.state.scores = [0, 1]
                    win_condition = True
            # If no win condition is satisfied, the game is a tie:
            if not win_condition:
                self.state.scores = [0.5, 0.5]
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
        :return: boolean determination of whether the game is finished or not
        """
        # If the board is full, the game is finished.
        if self.state.positions.count(0) == 0:
            return True
        # If the any win condition is satisfied, the game is finished.
        for condition in self.win_conditions:
            marks = [self.state.positions[i] for i in condition]
            if marks.count(1) == 3 or marks.count(2) == 3:
                return True
        # Otherwise, the game is not over.
        return False

    def agent_turn(self):
        """
        The agent_turn() method is a helper function to determine from the current state whose turn it is and whether
        any elements of the current state need to be masked before showing the agent.
        :return:
        """
        count_ones = self.state.positions.count(1)
        count_twos = self.state.positions.count(2)
        if count_ones == count_twos:
            # It's agent 1's turn:
            agent_index = 0
        else:
            # It's agent 2's turn:
            agent_index = 1
        # The partial state is just the state, since tic-tac-toe is perfect-information.
        partial_state = deepcopy(self.state)
        return agent_index, partial_state
