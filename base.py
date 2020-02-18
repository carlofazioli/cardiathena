import json
import uuid
from database import MySQLDatabase as db
from database.MySQLVariables import INSERT_STATE, INSERT_PLAYERS
from typing import List
from copy import deepcopy


class State:
    """
    State data structure contains a complete snapshot of the game at any time.
    """

class Action:
    """
    Action data structure contains a specification of the behavior of an agent.
    """


class Agent:
    """
    An Agent is an object (of arbitrary complexity) which makes a choice of Action when presented with a State.
    """

    def get_action(self,
                   partial_state: State):
        """
        The get_action() method somehow inspects the partial_state in order to determine which action to take.
        :param partial_state: A (potentially partial) state of the game.
        :return: an Action data structure specifying the agent's chosen behavior.
        """
        raise NotImplementedError


class Adjudicator:

    def __init__(self):
        """
        The Adjudicator is an encapsulation of the rules.  It tracks the ground truth state of a game in progress,
        updating when presented with agent actions.

        state: an instance of State data type representing the state of the game.
        """
        self.state: State = None

    def start_game(self):
        """
        The start_game() method creates a new State data type instance and manipulates it to represent the starting
        point for the game.
        :return: State instance
        """
        return self.state

    def step_game(self,
                  action: Action,
                  state: State):
        """
        Given an action by the agent whose turn it is, step_game() updates the state according to the rules and
        returns the new state.
        :param action: the Action of the Agent whose turn it is
        :param state: the current State of the game
        :return: the updated State
        """
        return self.state

    def get_state(self):
        """
        The get_state() method returns the current ground truth state of the game, used by the game manager to track
        the game history.  A separate call to agent_turn() indicates player turn and partial information.
        :return: the current state
        """
        return self.state

    def is_finished(self):
        """
        The is_finished() method is a helper function to determine when the game is over.
        :return: boolean determination of whether the game is finished or not
        """
        raise NotImplementedError

    def agent_turn(self):
        """
        The agent_turn() method is a helper function to determine from the current state whose turn it is and whether
        any elements of the current state need to be masked before showing the agent.
        :return:
        """
        raise NotImplementedError


class GameManager:
    def __init__(self,
                 agent_list: List[Agent],
                 adjudicator: Adjudicator,
                 state: State):
        """
        The GameManager controls game logic and moderates interactions between Agents and the Adjudicator.  The
        adjudicator stores the current game state, and updates it based on agent actions obtained by the GameManager
        from its agents.

        The GameManager also tracks that state/action histories of the game.

        The GameManager has helper functions to determine when the game is over, and if any partial information needs
        to be masked out before presenting the game state to agents.

        :param adjudicator: An adjudicator object
        :param agent_list: A list of Agent objects
        """
        self.adjudicator = adjudicator
        self.agent_list = agent_list
        self.state = state
        self.state_history = list()
        self.action_history = list()
        self.state_scores = list()
        self.game_uuid = uuid.uuid4().hex

    def play_game(self):
        """
        The play_game() method initializes the adjudicators internal state to the game's starting position.  It then
        iterates the turns of the game until finished, updating the state/action histories along the way.

        NOTE: this method likely does not need to be overridden in derived classes.
        :return: None
        """
        agents = list()
        for i in range(len(self.agent_list)):
            agents.append(str(self.agent_list[i]))

        if db.insert_players(INSERT_PLAYERS, self.game_uuid, json.dumps(agents)) is False:
            db.initialize_table()
            db.insert_players(INSERT_PLAYERS, self.game_uuid, json.dumps(agents))

        while not self.adjudicator.is_finished(self.state):
            # Make an empty list to handle however many actions we receive
            player_action = []
            # While the game is still in progress, inspect the current state to determine which agent should play,
            # and mask their state to hide any information.
            agent_index, partial_state = self.adjudicator.agent_turn(self.state)
            # Show the partial state to the current player and obtain their action.
            for i in range(len(agent_index)):
                # agent_turn will return two lists of the same size so go through them together
                current_player = self.agent_list[agent_index[i]]
                player_action.append(current_player.get_action(partial_state[i]))
            # Record this activity in the history.
            self.state_history.append(deepcopy(self.state))
            self.action_history.append(deepcopy(player_action))
            self.state_scores.append(deepcopy(self.state.get_state_scores()))
            # Adjudicate the action to receive an updated state.
            self.state = self.adjudicator.step_game(player_action, self.state)
        # At this point, the game is over.  Record the final state.
        self.state_history.append(deepcopy(self.state))
        self.action_history.append(0)
        self.state_scores.append(deepcopy(self.state.get_state_scores()))

    def save_game(self):
        """
        The save_game() method should process the state/action histories for the DB.

        :return:
        """
        state_values = list()
        action_values = list()
        score_values = list()
        num_of_states = len(self.state_history)

        for i in range(len(self.state_history)):
            state_values.append(self.state_history[i].get_state_values().tolist())

        for i in range(len(self.action_history)):
            action_values.append(str(self.action_history[i]))

        for i in range(len(self.state_scores)):
            score_values.append(str(self.state_scores[i]))

        for i in range(num_of_states):
            state_data = {
                'uuid': self.game_uuid,
                'states': state_values[i],
                'actions': action_values[i],
                'scores': score_values[i]
            }
            #print(state_data)

        for i in range(num_of_states):
            db.insert_state(INSERT_STATE,
                            self.game_uuid,
                            json.dumps(state_values[i]),
                            json.dumps(action_values[i]),
                            json.dumps(score_values[i]))
