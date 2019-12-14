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


# class Card:
#     suit = ''
#     card = ''
#
#     def set(self, suit, card):
#         """
#         inits the state and randomly assigns player
#
#         """
#         self.suit = suit
#         self.card = card


# class Deck:
#     cards = []
#
#     def shuffle_cards(self):
#         for s in suits:
#             for ct in cards:
#                 c = Card
#                 c.set(s, ct)
#                 cards.append(self, c)
#         shuffle(cards)
#
#     def get_top_card(self):
#         return cards.pop()


class State:

    def __init__(self):
        self.values = None


class HeartsState(State):
    """

    """

    # need a list of the players hands
    # need a deck of 52 cards that we are going to shuffle
    # players = [1] * 13 + [2] * 13 + [3] * 13 + [4] * 13
    #
    # def deal_cards(self):
    #     deck_of_cards = Deck
    #     deck_of_cards.shuffle_cards()
    #     for p in self.players:
    #         for i in p:
    #             i = deck_of_cards.get_top_card()

    # Stuff from SMEs (I think?), no clue what we're supposed to do with it

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

        return temp

    @property
    def card_position(self):
        """
        builds a python dictionary that lists the element position for each card on the state vector

        :return:
        """

        return {f'{v[1]}{v[0]}': i for i, v in enumerate(product(suits, cards))}
