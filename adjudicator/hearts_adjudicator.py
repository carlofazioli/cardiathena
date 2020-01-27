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
        self.lead_suit = -2
        self.pass_actions = []
        self.agent_types = []
        self.leading = 1

    def current_player(self):
        # Gets a list of all of the players, including the trick leader
        player_list = self.state.values[self.state.values > 20]
        if player_list is not None:
            # Getting the trick leader, can use this and the length of the player list to calculate current player
            # TODO: We may want to turn this into a call to the trick_leader function rather than calling it here!
            trick_leader = player_list[player_list > 30] % 10
            # What this line does:
            # Say trick_leader is 4, and players 1 and 2 have gone.
            # Add the length of the player list to 4, get 7.  Mod by 4, get 3
            current_player = (trick_leader + len(player_list)) % 4
        else:
            # TODO: This is a potential edge case which we may need to handle
            current_player = None
        # Returns the current player
        return current_player

    # TODO: This line may be enough to add into trick_leader, but we need to consider edge cases
    # return self.state.values[self.state.values > 30] % 10

    def trick_leader(self):
        # Returns the first player of the current trick
        cards_played = self.state.values[self.state.values > 20]
        if len(cards_played) == 0:
            print("empty")
        else:
            for x in range(4):
                found = cards_played[cards_played == (20 + 1 + x)]
                if len(found) == 1:
                    print(str(20 + 1 + x) + " exists")
        print(cards_played)
        return 0

    def lead_suit(self):
        # TODO: is there ever an instance where searching for the trick leader brings up null?
        trick_leader_card = np.where(self.state.values > 30)
        return int(trick_leader_card / 13)

    def cards_of_trick(self):
        return self.state.values[self.state.values > 20]
    # TODO: Do we even need this function?

    def trick_winner(self):
        # Returns the current player set to win the trick
        print(np.argmax(self.state.values == 21))
        print(np.argmax(self.state.values == 22))
        print(np.argmax(self.state.values == 23))
        print(np.argmax(self.state.values == 24))
        # players that have not played yet are going to get 0 even though they have not played that

        # find trick leader and use that to check who is in suit and who is not
        # largest one following trick is leader

    def trick_number(self):
        # Returns the trick number in the round
        played_count = 0
        played_count += (self.state.values == 11).sum()
        played_count += (self.state.values == 12).sum()
        played_count += (self.state.values == 13).sum()
        played_count += (self.state.values == 14).sum()
        played_count = int(played_count / 4)
        played_count += 1
        return played_count

    def points(self):
        # Returns a list of the points for each player in the current round
        points = [0, 0, 0, 0] #store the points here to return them
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
            print("stored trick_number: " + str(self.state.trick_number) + "\ncalculated trick_number: " + str(
                self.trick_number()))
            if self.state.trick_number == 0 and self.lead_suit == -2:
                self.pass_cards(action)
            else:
                # Add agent action to cards of tricks
                try:
                    self.state.cards_of_trick.append(action.card_index)
                except:
                    print("cards of check append fail")
                    print(self.state.values)
                    print("p: ", self.state.current_player)
                    print("trick_lead ", self.state.trick_winner)
                    print("suit_lead :", self.lead_suit)
                    print("action: ", action.card_index)
                # Update state with encoding for played in current trick
                if self.leading == 1:
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

                    # First card of trick has been played, remember the suit to make players follow it
                    if self.lead_suit == -1 or self.lead_suit == -2:
                        self.lead_suit = int(action.card_index / 13)

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
                if self.state.pass_type == 0:
                    player_to_pass = action + 1
                    # Loop around
                    if player_to_pass >= 5:
                        player_to_pass = 1

                # Pass 3 cards Counter-Clockwise(CCW) : 4,3,2,1...
                if self.state.pass_type == 1:
                    player_to_pass = action - 1
                    # Loop around
                    if player_to_pass <= 0:
                        player_to_pass = 4

                # Pass 3 cards Straight : 1 <-> 3 and 2 <-> 4
                if self.state.pass_type == 2:
                    player_to_pass = action + 2
                    # Loop around
                    if player_to_pass >= 5:
                        player_to_pass = player_to_pass - 4

                if self.state.pass_type == 3:
                    self.state.trick_number = 1
                    self.lead_suit = -2
                    self.state.current_player = self.state.values[0]
                    return self.state

                # Pass Cards
                for card_i in self.pass_actions[action - 1]:
                    self.state.values[card_i] = player_to_pass

            self.state.trick_number = 1
            self.lead_suit = -2
            self.state.current_player = self.state.values[0]

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
        trick_winner = self.state.values[max_card] % 10
        self.state.trick_winner = trick_winner

        print("trick winner:", trick_winner, " trick#:", self.state.trick_number, "  High card: ",
              max_card, " Points: ", self.points())

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
            self.update_score()
            self.state.trick_number = 0
            self.state.trick_winner = 0
            self.state.current_player = 1
            self.pass_actions.clear()
            self.lead_suit = -2
            self.state.pass_type += 1
            if self.state.pass_type > 3:
                self.state.pass_type = 0
            self.state.shuffle()
            #for i in range(len(self.state.score)):
             #   self.state.score[i] += self.state.points[i]
                #self.state.points[i] = 0

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
        print(self.trick_leader())

        # Mask only cards that belong to agent for passing
        if self.agent_passing(encode_state) is not None:
            return self.agent_passing(encode_state)

        # Make the two of clubs the only valid card if starting a round
        if self.first_trick(encode_state) is not None:
            return self.first_trick(encode_state)

        # Player can play any of their cards if they lead the trick (unless starting a round)
        if self.normal_trick(encode_state) is not None:
            return self.normal_trick(encode_state)

        # first hides values then changes returned ones if they can not be seen

        if self.check_suit(encode_state) is not None:
            return self.check_suit(encode_state)

    def hearts_broken(self):
        for i in range(39, 52):
            if self.state.values[i] > 10:
                # print("Hearts broken index=", i, " player cards=", self.state.values[i])
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

    def agent_passing(self, encode_state):
        """
        Masks encoding for the pass round.

        :returns current player
        :returns masked encoded state for pass round, None otherwise
        """
        if encode_state.trick_number == 0 and self.lead_suit == -2:
            encode_state.values = encode_state.hide_encoding(encode_state.current_player)
            return encode_state.current_player, encode_state
        else:
            return None

    def first_trick(self, encode_state):
        """
        Masks the encoding for the first trick where 2 of clubs must be played.

        :returns current player
        :returns masked encoded state
        """
        if encode_state.trick_number == 1 and self.lead_suit == -2:
            encode_state.values = encode_state.hide_encoding(encode_state.current_player)
            for i in range(len(encode_state.values)):
                if i != 0:
                    if encode_state.values[i] < 5:
                        # Turn values negative if they are held cards but not valid to play
                        encode_state.values[i] = encode_state.values[i] * (-1)
            return encode_state.current_player, encode_state

    def normal_trick(self, encode_state):
        """
        Masks the encoding for any trick other than the passing trick and the first trick. Factors in if hearts as been
        broken in the masked encoded state.

        :returns current player
        :returns masked encoded state
        """
        if self.lead_suit == -1:
            encode_state.values = encode_state.hide_encoding(encode_state.current_player)
            # Need to code in that players can not lead with any Hearts cards until that suit has been "broken"
            if not self.hearts_broken():
                # Check if player has anything other than hearts to play
                has_more_than_hearts = False
                for i in range(0, 39):
                    if encode_state.values[i] == encode_state.current_player:
                        has_more_than_hearts = True
                        break
                # Player only has hearts left, and must lead with it
                if not has_more_than_hearts:
                    return encode_state.current_player, encode_state
                for i in range(39, 52):
                    if encode_state.values[i] == encode_state.current_player:
                        encode_state.values[i] = encode_state.values[i] * (-1)
                return encode_state.current_player, encode_state
            return encode_state.current_player, encode_state

    def check_suit(self, encode_state):
        """
        Checks if player has suit or is void.

        :returns current player
        :returns masked encoded state
        """
        encode_state.values = encode_state.hide_encoding(encode_state.current_player)
        # beginning of range of valid cards
        begin = 13 * self.lead_suit
        # end of range of valid cards
        end = 13 * (self.lead_suit + 1)

        has_suit = False
        for i in range(begin, end):
            if 0 < encode_state.values[i] < 5:
                has_suit = True
        if not has_suit:
            # Player did not have suit and can play whatever
            return encode_state.current_player, encode_state
        # Encode it if we know they have valid cards
        for i in range(len(encode_state.values)):
            if i < begin or i >= end:
                if encode_state.values[i] < 5:
                    encode_state.values[i] = encode_state.values[i] * (-1)
        return encode_state.current_player, encode_state

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