import numpy as np
from itertools import product
from random import shuffle

# definitions for the card values and suit values in a 52 card deck
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'S', 'H']

# constants
player_hand = [1, 2, 3, 4]
player_won = [11, 12, 13, 14]
player_current = [21, 22, 23, 24]
unknown = 0


class State:

    def __init__(self):
        # Probably want to change values to something else to reflect Adjudicator doc (Card deck?)
        self.values = None
        self.score = [0, 0, 0, 0]


class HeartsState(State):
    """

    """

    def __init__(self):
        """
        inits the state and randomly assigns player

        """

        super().__init__()
        self.shuffle()
        # Game Logic
        self.current_player = 1
        self.trick_number = 0
        self.trick_winner = 0
        self.pass_type = 0
        self.cards_of_trick = []
        self.points = [0, 0, 0, 0] #points for a round rather than a game

    def __repr__(self):
        """
        the human readable representation of the state vector

        :return: string
        """
        out = '|'.join([f'{x:>3}' for x in self.card_position.keys()]) + "\n" + '|'.join(
            [f'{x:3}' for x in self.values])

        return out

    def shuffle(self):
        players = [1] * 13 + [2] * 13 + [3] * 13 + [4] * 13
        shuffle(players)
        self.values = np.array(players)

    def set_encoding(self, encoding, card):
        """
        encode a value to the state vector

        :param encoding: value to be encoded on the state vector
        :param card: position in the state vector the be encoded
        :return: None
        """

        element = self.card_position[card]
        self.values[element] = encoding

    def get_encoding(self, card):
        """

        :param card: position in the state vector to get value
        :return: encoded value
        """
        element = self.card_position[card]

        return self.values[element]

    def hide_encoding(self, player):
        """
         Mask state vector values replacing hidden information with zeros.

         :param player: the player number 1-4 to receive a tailored masked encoding state vector
         :return: masked encoding np array
         """

        held_cards = self.values == player
        played_cards = self.values > 10
        temp = np.where(held_cards+played_cards, self.values, np.zeros(52, dtype=int))
        #print(temp)
        #currently not differentiating between valid cards and invalid cards so agents are playing any of the cards in their hands

        return temp

    def store_values(self):

        store_value = list(self.values)
        store_value = store_value + self.score
        store_value.append(self.current_player)
        store_value.append(self.trick_number)
        store_value.append(self.trick_winner)
        store_value.append(self.pass_type)
        store_value = store_value + self.points

        return store_value

    def store_strings(self):

        store_string = []
        for i in range(52): #label indices for storage of values
            store_string.append(i)
        for i in range(4): #label numbers of players for storage of score
            store_string.append("Score of " + str(i))
        game_logic = ["Current Player","Trick Number","Trick Winner","Pass Type"]
        for i in range(4):
            game_logic.append("Points of " + str(i))
        store_string = store_string + game_logic

        return store_string

    @property
    def card_position(self):
        """
        builds a python dictionary that lists the element position for each card on the state vector

        :return:
        """

        return {f'{v[1]}{v[0]}': i for i, v in enumerate(product(suits, cards))}
