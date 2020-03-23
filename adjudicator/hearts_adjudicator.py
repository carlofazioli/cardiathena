import copy

import numpy as np

from adjudicator.state import HeartsState
from agent.RandomHeartsAgent import HeartsAction
from base import *


class HeartsAdjudicator(Adjudicator):
    """
    The Adjudicator is an encapsulation of the rules.  It tracks the ground truth state of a game in progress,
    updating when presented with agent actions.

    state: an instance of State data type representing the state of the game.
    """

    def __init__(self):
        super().__init__()

    def current_player(self,
                       state: HeartsState):
        # Gets a list of all of the players, including the trick leader
        player_list = state.values[state.values > 20]
        # Calculate who goes next
        if 0 < len(player_list) < 4:
            # Getting the trick leader, can use this and the length of the player list to calculate current player
            trick_leader = self.trick_leader(state)
            # What this line does:
            # Say trick_leader is 4, and players 1 and 2 have gone.
            # Add the length of the player list to 4, get 7.  Mod by 4, get 3
            current_player = (trick_leader + len(player_list))
            if current_player > 4:
                # 4 % 4 is 0 and we do not want that
                current_player = current_player % 4
            # was returning a list instead of a number, can change later if needed but causing issues now
            current_player = current_player[0]
        else:
            # Either no one has played yet or everyone has played
            if self.trick_number(state) == 1 and (state.values > 10).sum() == 0:
                # Return the owner of the two of clubs if this is the first card of the first trick
                return state.values[0]
            return self.trick_winner(state)
        # Returns the current player
        return current_player

    def trick_leader(self,
                     state: HeartsState):
        # Returns the first player of the current trick
        trick_lead = state.values[state.values > 30]

        if len(trick_lead) == 0:
            return None
        return trick_lead % 10

    def lead_suit(self,
                  state: HeartsState):
        # Getting the card index of the trick leader
        trick_leader_card = np.where(state.values > 30)
        # If there is no trick leader card
        if len(trick_leader_card[0]) == 0:
            if self.trick_number(state) >= 1:
                # -1 means there needs to be a new leader
                # should no longer come in here
                return -1
        return int(trick_leader_card[0] / 13)

    def cards_of_trick(self,
                       state: HeartsState):
        return np.where(state.values > 20)[0]

    def trick_winner(self,
                     state: HeartsState):
        # Returns the current player set to win the trick
        played_cards = self.cards_of_trick(state)
        suit = self.lead_suit(state)
        # We do not have a trick_winner
        if len(played_cards) == 0 and suit is None:
            return None
        max_card = -1
        for i in played_cards:
            if (i > max_card) and (int(i / 13) == suit):
                max_card = i
        return state.values[max_card] % 10

    def trick_number(self,
                     state: HeartsState):
        # Returns the trick number in the round
        if self.is_passing(state):
            return 0
        played_count = (state.values > 10).sum()
        played_count = int(played_count / 4)
        played_count += 1

        return played_count

    def is_passing(self,
                   state: HeartsState):
        # A function that returns whether the players are currently passing

        if state.pass_type > 0:
            return True # The players should pass
        return False # negative or 0 which represents not passing

    def points(self,
               state: HeartsState):
        # Returns a list of the points for each player in the current round
        
        # store the points here to return them
        points = [0, 0, 0, 0]
        for i in range(4):
            # Loop through the four players to find the cards they own
            owned = state.values == 11 + i # Returns True for all the cards owned by the player
            if owned[36] == True:
                points[i] += 13 # 13 points for the queen of spades
            for j in range(39, 52, 1):
                if owned[j] == True:
                    points[i] += 1 # Add one point for each heart which are found in the range 39-52
        return points

    def update_score(self,
                     state: HeartsState):
        # Updates the scores of all the players by using the points and determining if anyone shot for the moon
        points = self.points(state)
        
        if points.count(26) > 0:
            # If anyone has 26, they got all the points and successfully shot for the moon
            winner = points.index(26) # Only find the index of 26 if it exists
            for i in range(4):
                if i != winner: # The winner does not get 26 added to their score
                    state.score[i] += 26
        else:
            # No players successfuly shot for the moon so points are added normally
            for i in range(4):
                state.score[i] += points[i]

    def start_game(self):
        """
        The start_game() method creates a new State data type instance and manipulates it to represent the starting
        point for the game.

        :return: State instance
        """
        # Hearts objects already initialize to the starting position.
        # self.state = HeartsState()

        # return self.state
        return None

    def step_game(self,
                  actions: HeartsAction,
                  state: HeartsState):
        """
        Given an action by the agent whose turn it is, step_game() updates the state according to the rules and
        returns the new state.

        :param actions: the Action of the Agent whose turn it is
        :param state: the current State of the game
        :return: the updated State
        """
        state_copy = deepcopy(state)
        # Check if game is finished
        if self.is_finished(state_copy):
            print("original is finished check")
            return self.state_copy
        else:
            # Loop through the list of actions
            for act_num in range(len(actions)):
                # Players passing their cards is the only time there are simultaneous actions
                if self.is_passing(state_copy):
                    # act_num represents the player that owns the action
                    # act_num and actions range from 0-3 even though players are 1-4
                    # so we add one to act_num to represent the actual player number
                    self.pass_cards(actions[act_num], act_num + 1, state_copy)
                else:
                    # Check the current state for when trick is over
                    if self.is_trick_over(state_copy):
                        self.end_of_trick(state_copy)
                    # Update state with encoding for played in current trick
                    if self.trick_leader(state_copy) is None:
                        # check if leading and make 31-34 for leader
                        state_copy.values[actions[act_num].card_index] = (30 + state_copy.values[actions[act_num].card_index])
                    else:
                        # regular plays that are not leading are 21-24
                        state_copy.values[actions[act_num].card_index] = (20 + state_copy.values[actions[act_num].card_index])
                    #
                    # Check if new round, update score and deal new cards if so
                    if self.is_round_over(state_copy):
                        self.new_round(state_copy)

        return state_copy

    def pass_cards(self,
                   action: HeartsAction,
                   player: int,
                   state: HeartsState):
        """
        Handles the passing cards at the beginning of each round. Swaps cards once all 4 players have chosen three
        cards to pass.

        :param action: the Action of the Agent whose turn it is
        :returns unaltered state for non passing round, otherwise returns nothing.
        """
        # Implement pass here

        # Pass cards to player_to_pass

        # Pass 3 cards Clockwise(CW) : 1,2,3,4...
        if state.pass_type == 1:
            # Add one to the player number to find the player CW to them
            player_to_pass = player + 1
            # Loop around
            if player_to_pass >= 5:
                player_to_pass = 1

        # Pass 3 cards Counter-Clockwise(CCW) : 4,3,2,1...
        if state.pass_type == 2:
            # Subtract one from the player number to find the player CCW to them
            player_to_pass = player - 1
            # Loop around
            if player_to_pass <= 0:
                player_to_pass = 4

        # Pass 3 cards Straight : 1 <-> 3 and 2 <-> 4
        if state.pass_type == 3:
            # Add two to find the player across
            player_to_pass = player + 2
            # Loop around
            if player_to_pass >= 5:
                # If adding two went too far, we should have subtracted two instead
                player_to_pass = player_to_pass - 4

        # Pass Cards
        for card_i in action.card_index:
            state.values[card_i] = player_to_pass

        # We know all players have passed when the fourth player has since we always start passing with the first player
        if player == 4:
            # Make the value negative so we know to no longer pass the cards until the beginning of next trick
            if state.pass_type > 0:
                state.pass_type = state.pass_type * -1

    def end_of_trick(self,
                     state: HeartsState):
        """
        Function handles the end of a trick which entails tallying up points, determining the trick winner,
        setting the current player, and incrementing the pass type.
        """

        # Find max card and then find the owner of the card
        max_card = self.find_max_card(state)
        trick_winner = self.trick_winner(state)

        # All of these cards belong to the trick winner (tricks won)
        for card in self.cards_of_trick(state):
            state.values[card] = trick_winner + 10

        print("trick winner:", trick_winner, " trick#:", self.trick_number(state) - 1, "  High card: ",
              max_card, " Points: ", self.points(state))

    def new_round(self,
                  state: HeartsState):
        """
        At the end of the round, the points should be distributed properly
        and the deck should be reshuffled to play again
        """

        # Give the trick_winner their cards before wrapping up this round
        trick_winner = self.trick_winner(state)
        for card in self.cards_of_trick(state):
            state.values[card] = trick_winner + 10
        
        # Print final results
        print("trick winner:", trick_winner, " trick#:", self.trick_number(state) - 1,
              " Points: ", self.points(state))
        
        # Update the score
        self.update_score(state)
        if self.is_finished(state):
            # Do not shuffle if game is over
            return

        # New round, shuffle cards, and Pass cards
        state.shuffle()
        
        # Make the value positive to show that we will be passing (unless zero because 0 * -1 is 0)
        if state.pass_type < 0:
            state.pass_type = state.pass_type * -1
            
        state.pass_type += 1
        if state.pass_type > 3:
            state.pass_type = 0
    
    def get_state(self):
        """
        :return: the current state
        """
        return None

    def is_finished(self,
                    state: HeartsState):
        """
        The is_finished() method is a helper function to determine when the game is over.
        The game is over when the first player has reached 100 or more points
        :return: boolean determination of whether the game is finished or not
        """
        for i in range(0, 4):
            if state.score[i] >= 100:

                print("P1: ", state.score[0],
                  " P2: ", state.score[1],
                  " P3: ", state.score[2],
                  " P4: ", state.score[3])
                return True
        return False

    def agent_turn(self,
                   state: HeartsState):
        """
        The agent_turn() method is a helper function to determine from the current state whose turn it is and whether
        any elements of the current state need to be masked before showing the agent.
        :return: player index and a masked state
        """
        # copy of the state to manipulate for the agent
        encode_state = copy.deepcopy(state)

        # Mask only cards that belong to agent for passing
        if self.is_passing(state):
            # Players passing will be the only time players play simultaneously in hearts
            return self.agent_passing(state)

        # Make the two of clubs the only valid card if starting a round
        if self.first_trick(encode_state) is not None:
            encode_state = copy.deepcopy(state)
            return self.first_trick(encode_state)

        # Still starting a round, but the two of clubs has already been played.
        # Need to make sure that the players do not play any Hearts cards or the Queen of Spades
        # during the first trick.
        if self.first_trick_cancel_queen_hearts(encode_state) is not None:
            encode_state = copy.deepcopy(state)
            return self.first_trick_cancel_queen_hearts(encode_state)

        # Player can play any of their cards if they lead the trick (unless starting a round)
        if self.is_trick_over(state):
            # A state with the info of the trick winner is given to determine leader
            encode_state = copy.deepcopy(state)
            return self.lead_trick(encode_state)

        if self.check_suit(encode_state) is not None:
            encode_state = copy.deepcopy(state)
            return self.check_suit(encode_state)

    def hearts_broken(self,
                      state: HeartsState):
        for i in range(39, 52):
            if state.values[i] > 10:
                return True
        return False

    def is_trick_over(self,
                      state: HeartsState):
        """
        Checks the current state for encoded values 21 to 34 to determine if the trick is over.

        :returns True if trick is over, False otherwise
        """
        if len(list(x for x in state.values if 21 <= x <= 34)) >= 4:
            return True
        return False

    def is_round_over(self,
                      state: HeartsState):
        """
        Check if the round is over by looking at the trick number

        :returns True if round is over, Fasle otherwise
        """
        if self.trick_number(state) > 13:
            return True
        return False

    def find_max_card(self,
                      state: HeartsState):
        """
        Finds the highest value card based off the lead suit.

        :returns the max suited card
        """
        begin = 13 * self.lead_suit(state)  # beginning of range of valid cards
        end = 13 * (self.lead_suit(state) + 1)  # end of range of valid cards

        card_max = 0

        if begin < 0 and end < 0:
            card_max = self.cards_of_trick()[0]
        else:
            for x in self.cards_of_trick(state):
                if begin <= x < end:
                    if x > card_max:
                        card_max = x
        return card_max

    def agent_passing(self, encode_state):
        """
        Masks encoding for the pass round.

        :returns current player
        :returns masked encoded state for pass round, None otherwise
        """
        if self.trick_number(encode_state) == 0 and self.is_passing(encode_state):
            # All the players will pass simultaneously so get their encode_values
            players = [1, 2, 3, 4]
            encode_values = []
            for player in players:
                # Get each encode value and store it
                store_state = copy.deepcopy(encode_state)
                store_state.values = store_state.hide_encoding(player)
                encode_values.append(store_state)
            return players, encode_values
        else:
            return None

    def first_trick(self, encode_state):
        """
        Masks the encoding for the first trick where 2 of clubs must be played.

        :returns current player
        :returns masked encoded state
        """
        encode_state_copy = copy.deepcopy(encode_state)
        if self.trick_number(encode_state) == 1 and (encode_state.values > 10).sum() == 0:
            player = self.current_player(encode_state)
            encode_state_copy.values = encode_state_copy.hide_encoding(player)
            for i in range(len(encode_state_copy.values)):
                if i != 0:
                    if encode_state_copy.values[i] < 5:
                        # Turn values negative if they are held cards but not valid to play
                        encode_state_copy.values[i] = encode_state_copy.values[i] * (-1)
            return [player], [encode_state_copy]

    def first_trick_cancel_queen_hearts(self, encode_state):
        """
        Masks the encoding for all of the hearts and queen of spades cards for the first trick.

        :returns current player
        :returns masked encoded state
        """
        encode_state_copy = copy.deepcopy(encode_state)
        if self.trick_number(encode_state_copy) == 1:
            player = self.current_player(encode_state)
            encode_state_copy.values = encode_state_copy.hide_encoding(player)
            card_index = 0
            for _ in encode_state_copy.values:
                if card_index == 36 or 51 >= card_index >= 39:
                    if encode_state_copy.values[card_index] < 5:
                        # Turn values negative if they are held cards but not valid to play
                        encode_state_copy.values[card_index] = encode_state_copy.values[card_index] * (-1)
                card_index = card_index + 1
            return [player], [encode_state_copy]

    def lead_trick(self, encode_state):
        """
        Masks the encoding for a player leading the trick

        :returns current player
        :returns masked encoded state
        """
        state = copy.deepcopy(encode_state)
        encode_state.values = encode_state.hide_encoding(self.current_player(state))
        if not self.hearts_broken(state):
            # Check if player has anything other than hearts to play
            has_more_than_hearts = False
            for i in range(0, 39):
                if encode_state.values[i] == self.current_player(state):
                    has_more_than_hearts = True
                    break
                # Player only has hearts left, and must lead with it
            if not has_more_than_hearts:
                return [self.current_player(state)], [encode_state]
            for i in range(39, 52):
                if encode_state.values[i] == self.current_player(state):
                    encode_state.values[i] = encode_state.values[i] * (-1)
            return [self.current_player(state)], [encode_state]
        return [self.current_player(state)], [encode_state]

    def check_suit(self, encode_state):
        """
        Checks if player has suit or is void.

        :returns current player
        :returns masked encoded state
        """
        encode_state_copy = copy.deepcopy(encode_state)
        # encode_state_copy.values = encode_state_copy.hide_encoding(encode_state_copy.current_player)
        encode_state_copy.values = encode_state_copy.hide_encoding(self.current_player(encode_state))
        # beginning of range of valid cards
        begin = 13 * self.lead_suit(encode_state)
        # end of range of valid cards
        end = 13 * (self.lead_suit(encode_state) + 1)

        has_suit = False
        for i in range(begin, end):
            if 0 < encode_state_copy.values[i] < 5:
                has_suit = True
        if not has_suit:
            # Player did not have suit and can play whatever
            return [self.current_player(encode_state)], [encode_state_copy]
        # Encode it if we know they have valid cards
        for i in range(len(encode_state_copy.values)):
            if i < begin or i >= end:
                if encode_state_copy.values[i] < 5:
                    encode_state_copy.values[i] = encode_state_copy.values[i] * (-1)
        return [self.current_player(encode_state)], [encode_state_copy]

    """def check_update_score(self, string):
        if string == "moon":
            # Checking for shooting for the moon
            new_state = HeartsState()
            for i in range(len(new_state.values)):
                new_state.values[i] = 11
        else:
            new_state = HeartsState()
            for i in range(len(new_state.values)):
                new_state.values[i] = 11
            new_state.values[36] = 12
        self.state = new_state
        print(self.state.score)
        self.update_score()
        print(self.state.score)"""