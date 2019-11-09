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
        self.values = None


class HeartsState(State):

    """

    """

    def __init__(self):
        """
        inits the state and randomly assigns player

        """
        super().__init__()
        self.shuffle()

    def __repr__(self):
        """
        the human readable representation of the state vector

        :return: string
        """
        out = '|'.join([f'{x:>3}' for x in self.card_position.keys()]) + "\n" + '|'.join([f'{x:3}' for x in self.values])

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
        player_1 = [1, 11, 21]
        player_2 = [2, 12, 22]
        player_3 = [3, 13, 23]
        player_4 = [4, 14, 24]
        players = [player_1, player_2, player_3, player_4]
        ret = []
        for x in self.values:
            if x in players[player]:
                ret.append(x)
            else:
                ret.append(0)
        return np.array(ret)


    @property
    def card_position(self):
        """
        builds a python dictionary that lists the element position for each card on the state vector

        :return:
        """

        return {f'{v[1]}{v[0]}': i for i, v in enumerate(product(suits, cards))}


