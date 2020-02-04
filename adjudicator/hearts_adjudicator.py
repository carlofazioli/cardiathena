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
        # A variable that will range from 0-3 to determine the leading suit;
        # -2 for beginning of round after pass; -1 for rest of trick starts
        self.pass_actions = []
        self.agent_types = []
        self.leading = 1

    def current_player(self):
        # Gets a list of all of the players, including the trick leader
        player_list = self.state.values[self.state.values > 20]
        if len(player_list) != 0:
            # Getting the trick leader, can use this and the length of the player list to calculate current player
            trick_leader = self.trick_leader()
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
            '''From Angela about the validity of this edge case: This all depends on how we handle changing the state but if this edge case does happen, we know it is 
            because the leader has not played yet and needs to choose a card. If we go this path, we might want to 
            use the suggestion Michael made where we mark the winner from the last state with a placeholder 31-34 
            until after they have made their decision, at which point we assign their past card properly and set the 
            card they chose. '''
            if self.trick_number() == 1 and (self.state.values > 10).sum() == 0:
                # Return the owner of the two of clubs if this is the first card of the first trick
                return self.state.values[0]
            return self.state.current_player
            current_player = None
        # Returns the current player
        return current_player

    def trick_leader(self):
        # Returns the first player of the current trick
        trick_lead = self.state.values[self.state.values > 30]
        if len(trick_lead) == 0:
            return None
        return trick_lead % 10

    # TODO: rename this back to "lead_suit". apparently python doesnt like that we have a variable and function
    # TODO: with the same name

    def alead_suit(self):
        # TODO: when we do simultaneous passing this will need to change
        # Getting the card index of the trick leader
        trick_leader_card = np.where(self.state.values > 30)
        # If there is no trick leader card
        if len(trick_leader_card[0]) == 0:
            if self.trick_number() >= 1:
                # -1 means there needs to be a new leader
                return -1
        return int(trick_leader_card[0] / 13)

    def cards_of_trick(self):
        return np.where(self.state.values > 20)[0]

    def trick_winner(self):
        # Returns the current player set to win the trick
        played_cards = self.cards_of_trick()
        suit = self.alead_suit()
        # We do not have a trick_winner
        if len(played_cards) == 0 and suit is None:
            return None
        max_card = -1
        for i in played_cards:
            if (i > max_card) and (int(i / 13) == suit):
                max_card = i
        return self.state.values[max_card] % 10

    def trick_number(self):
        # Returns the trick number in the round
        played_count = (self.state.values > 10).sum()
        if self.is_passing():
            return 0
        played_count = int(played_count / 4)
        played_count += 1

        return played_count

    def is_passing(self):
        # A function that returns whether the players are currently passing

        if self.state.pass_type > 0:
            return True # The players should pass
        return False # negative or 0 which represents not passing

    def points(self):
        # Returns a list of the points for each player in the current round
        
        # store the points here to return them
        points = [0, 0, 0, 0]
        for i in range(4):
            # Loop through the four players to find the cards they own
            owned = self.state.values == 11 + i # Returns True for all the cards owned by the player
            if owned[36] == True:
                points[i] += 13 # 13 points for the queen of spades
            for j in range(39, 52, 1):
                if owned[j] == True:
                    points[i] += 1 # Add one point for each heart which are found in the range 39-52
        return points

    def update_score(self):
        # Updates the scores of all the players by using the points and determining if anyone shot for the moon
        points = self.points()
        
        if points.count(26) > 0:
            # If anyone has 26, they got all the points and successfully shot for the moon
            winner = points.index(26) # Only find the index of 26 if it exists
            for i in range(4):
                if i != winner: # The winner does not get 26 added to their score
                    self.state.score[i] += 26
        else:
            # No players successfuly shot for the moon so points are added normally
            for i in range(4):
                self.state.score[i] += points[i]

    def start_game(self):
        """
        The start_game() method creates a new State data type instance and manipulates it to represent the starting
        point for the game.

        :return: State instance
        """
        # Hearts objects already initialize to the starting position.
        self.state = HeartsState()

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
            print("calculated trick_number: " + str(self.trick_number()))
            if self.is_passing():
                self.pass_cards(action)
            else:
                # Update state with encoding for played in current trick
                if self.trick_leader() is None:
                    # if self.leading == 1:
                    # check if leading and make 31-34 for leader
                    self.state.values[action.card_index] = (30 + self.state.values[action.card_index])
                    self.leading = 0 # no more leading
                else:
                    # regular plays that are not leading are 21-24
                    self.state.values[action.card_index] = (20 + self.state.values[action.card_index])
                #
                # Content in the "trick is over" if-statement can be a function.
                #
                # Check the current state for when trick is over
                if self.is_trick_over():
                    self.end_of_trick()
                else:
                    # Normal trick play, set next player
                    self.state.current_player = self.state.current_player + 1
                    if self.state.current_player == 5:
                        self.state.current_player = 1

        return self.state

    def pass_cards(self, action: HeartsAction):
        """
        Handles the passing cards at the beginning of each round. Swaps cards once all 4 players have chosen three
        cards to pass.

        :param action: the Action of the Agent whose turn it is
        :returns unaltered state for non passing round, otherwise returns nothing.
        """
        # Implement pass here
        self.pass_actions.append(action.card_index)
        # Set next player to pass three cards
        self.state.current_player = self.state.current_player + 1

        # All players have chosen cards to pass
        if len(self.pass_actions) > 3:
            # prepare found agent to handle two of clubs at beginning of round
            # Pass cards to player_to_pass
            for action in range(len(self.pass_actions)):
                player_to_pass = 0
                # action starts from 0 while players start from 1
                action += 1

                # Pass 3 cards Clockwise(CW) : 1,2,3,4...
                if self.state.pass_type == 1:
                    player_to_pass = action + 1
                    # Loop around
                    if player_to_pass >= 5:
                        player_to_pass = 1

                # Pass 3 cards Counter-Clockwise(CCW) : 4,3,2,1...
                if self.state.pass_type == 2:
                    player_to_pass = action - 1
                    # Loop around
                    if player_to_pass <= 0:
                        player_to_pass = 4

                # Pass 3 cards Straight : 1 <-> 3 and 2 <-> 4
                if self.state.pass_type == 3:
                    player_to_pass = action + 2
                    # Loop around
                    if player_to_pass >= 5:
                        player_to_pass = player_to_pass - 4

                # Pass Cards
                for card_i in self.pass_actions[action - 1]:
                    self.state.values[card_i] = player_to_pass

            self.state.current_player = self.state.values[0]
            # Make the value negative so we know to no longer pass the cards until the beginning of next trick
            if self.state.pass_type > 0:
                self.state.pass_type = self.state.pass_type * -1

            # Testing for adjudicator trick_winner
            # self.trick_winner()

    def end_of_trick(self):
        """
        Function handles the end of a trick which entails tallying up points, determining the trick winner,
        setting the current player, and incrementing the pass type.
        """
        # prepare to lead in next trick
        self.leading = 1

        # the points accumulated for the current trick
        trick_points = 0

        # Find max card and then find the owner of the card
        max_card = self.find_max_card()
        atrick_winner = self.state.values[max_card] % 10
        trick_winner = self.trick_winner()
        # self.state.trick_winner = trick_winner

        print("trick winner:", trick_winner, " trick#:", self.trick_number(), "  High card: ",
              max_card, " Points: ", self.points())

        # Check for point cards (Queen of Spades and Hearts)
        for i in self.cards_of_trick():
            # 36 is the index of the Queen of spades
            if i == 36:
                trick_points = trick_points + 13
            # 39 and up are the indices for hearts
            if i >= 39:
                trick_points = trick_points + 1

        # Update state points
        self.state.points[trick_winner - 1] = self.state.points[trick_winner - 1] + trick_points

        # All of these cards belong to the trick winner (tricks won)
        for card in self.cards_of_trick():
            self.state.values[card] = trick_winner + 10

        # Clear out the cards in current trick
        # self.state.cards_of_trick.clear()

        # Trick winner should be set up to start next trick
        # self.state.current_player = self.state.trick_winner
        self.state.current_player = trick_winner

        # Check if new round, reset trick_number and deal new cards
        if self.trick_number() > 13:
            self.new_round()

    def new_round(self):
        # New round, shuffle cards, and Pass cards
        self.update_score()
        # self.state.trick_winner = 0
        self.state.current_player = 1
        self.pass_actions.clear()
        self.state.pass_type += 1
        if self.state.pass_type > 3:
            self.state.pass_type = 0
        self.state.shuffle()
        
        # Make the value positive to show that we will be passing (unless zero because 0 * -1 is 0)
        if self.state.pass_type < 0:
            self.state.pass_type = self.state.pass_type * -1
    
    def get_state(self):
        """
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
        #if self.agent_passing(encode_state) is not None:
        if self.is_passing():
            return self.agent_passing(encode_state)

        # Make the two of clubs the only valid card if starting a round
        if self.first_trick(encode_state) is not None:
            encode_state = copy.deepcopy(self.state)
            return self.first_trick(encode_state)

        # Player can play any of their cards if they lead the trick (unless starting a round)
        if self.lead_trick(encode_state) is not None:
            encode_state = copy.deepcopy(self.state)
            return self.lead_trick(encode_state)

        # first hides values then changes returned ones if they can not be seen

        if self.check_suit(encode_state) is not None:
            encode_state = copy.deepcopy(self.state)
            return self.check_suit(encode_state)

    def hearts_broken(self):
        for i in range(39, 52):
            if self.state.values[i] > 10:
                return True
        return False

    def is_trick_over(self):
        """
        Checks the current state for encoded values 21 to 34 to determine if the trick is over.

        :returns True if trick is over, False otherwise
        """
        if len(list(x for x in self.state.values if 21 <= x <= 34)) >= 4:
            return True
        return False

    def find_max_card(self):
        """
        Finds the highest value card based off the lead suit.

        :returns the max suited card
        """
        begin = 13 * self.alead_suit()  # beginning of range of valid cards
        end = 13 * (self.alead_suit() + 1)  # end of range of valid cards

        card_max = 0

        if begin < 0 and end < 0:
            card_max = self.cards_of_trick()[0]
        else:
            for x in self.cards_of_trick():
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
        if self.trick_number() == 0 and self.is_passing():
            encode_state.values = encode_state.hide_encoding(self.current_player())
            return self.current_player(), encode_state
        else:
            return None

    def first_trick(self, encode_state):
        """
        Masks the encoding for the first trick where 2 of clubs must be played.

        :returns current player
        :returns masked encoded state
        """
        encode_state_copy = copy.deepcopy(encode_state)
        if self.trick_number() == 1 and (self.state.values > 10).sum() == 0:
            player = self.current_player()
            encode_state_copy.values = encode_state_copy.hide_encoding(player)
            for i in range(len(encode_state_copy.values)):
                if i != 0:
                    if encode_state_copy.values[i] < 5:
                        # Turn values negative if they are held cards but not valid to play
                        encode_state_copy.values[i] = encode_state_copy.values[i] * (-1)
            return player, encode_state_copy

    def lead_trick(self, encode_state):
        """
        Masks the encoding for a player leading the trick

        :returns current player
        :returns masked encoded state
        """
        encode_state_copy = copy.deepcopy(encode_state)
        if self.alead_suit() == -1:
            encode_state.values = encode_state.hide_encoding(self.current_player())
            # Need to code in that players can not lead with any Hearts cards until that suit has been "broken"
            if not self.hearts_broken():
                # Check if player has anything other than hearts to play
                has_more_than_hearts = False
                for i in range(0, 39):
                    if encode_state.values[i] == self.current_player():
                        has_more_than_hearts = True
                        break
                # Player only has hearts left, and must lead with it
                if not has_more_than_hearts:
                    return self.current_player(), encode_state
                for i in range(39, 52):
                    if encode_state.values[i] == self.current_player():
                        encode_state.values[i] = encode_state.values[i] * (-1)
                return self.current_player(), encode_state
            return self.current_player(), encode_state

    def check_suit(self, encode_state):
        """
        Checks if player has suit or is void.

        :returns current player
        :returns masked encoded state
        """
        encode_state_copy = copy.deepcopy(encode_state)
        # encode_state_copy.values = encode_state_copy.hide_encoding(encode_state_copy.current_player)
        encode_state_copy.values = encode_state_copy.hide_encoding(self.current_player())
        # beginning of range of valid cards
        begin = 13 * self.alead_suit()
        # end of range of valid cards
        end = 13 * (self.alead_suit() + 1)

        has_suit = False
        for i in range(begin, end):
            if 0 < encode_state_copy.values[i] < 5:
                has_suit = True
        if not has_suit:
            # Player did not have suit and can play whatever
            return self.current_player(), encode_state_copy
        # Encode it if we know they have valid cards
        for i in range(len(encode_state_copy.values)):
            if i < begin or i >= end:
                if encode_state_copy.values[i] < 5:
                    encode_state_copy.values[i] = encode_state_copy.values[i] * (-1)
        return self.current_player(), encode_state_copy

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