import numpy as np
from itertools import product
from random import shuffle
from base import State
# definitions for the card values and suit values in a 52 card deck
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits = ['C', 'D', 'S', 'H']

# constants
player_hand = [1, 2, 3, 4]
player_won = [11, 12, 13, 14]
player_current = [21, 22, 23, 24]
trick_leader = [31, 32, 33, 34]
unknown = 0


class HeartsState(State):
    """

    """

    def __init__(self):
        """
        inits the state and randomly assigns player

        """
        super().__init__()
        self.deck = None
        self.score = [0, 0, 0, 0]
        self.shuffle()
        self.pass_type = 1
        self.points = [0, 0, 0, 0] #points for a round rather than a game


        #What we are defining as points for the game. Here we have the indices for all the hearts as well as the
        #queen of spade
        self.points_cond = [ 36,39,40,41,42,43,44,45,46,47,48,49,50,51,52]


    def __repr__(self):
        """
        the human readable representation of the state vector

        :return: string
        """
        out = '|'.join([f'{x:>3}' for x in self.card_position.keys()]) + "\n" + '|'.join(
            [f'{x:3}' for x in self.deck])

        return out

    def get_state_deck(self):
        return self.deck

    def get_state_scores(self):
        return self.score

    def shuffle(self):
        """
        Creates a new deck with 13 random cards for every player
        
        :return: None
        """
        players = [1] * 13 + [2] * 13 + [3] * 13 + [4] * 13
        shuffle(players)
        self.deck = np.array(players)

    def set_encoding(self, encoding, card):
        """
        encode a value to the state vector

        :param encoding: value to be encoded on the state vector
        :param card: position in the state vector the be encoded
        :return: None
        """
        element = self.card_position[card]
        self.deck[element] = encoding

    def get_encoding(self, card):
        """

        :param card: position in the state vector to get value
        :return: encoded deck
        """
        element = self.card_position[card]

        return self.deck[element]

    def hide_encoding(self, player):
        """
         Mask state vector deck replacing hidden information with zeros.

         :param player: the player number 1-4 to receive a tailored masked encoding state vector
         :return: masked encoding np array
         """
        # currently not differentiating between valid cards and invalid cards so agents are playing any of the cards in their hands
        held_cards = self.deck == player
        played_cards = self.deck > 10
        return np.where(held_cards+played_cards, self.deck, np.zeros(52, dtype=int))

    def save_state(self, player_action):
        """
        The save_state(player_action) method is called from the GameManager's play_game(). At any point the state of
        the game changes via player actions, this method returns a snapshot of the state. The method returns a
        dictionary: state_data, which contains the location of the cards: deck, player actions, and the score.

        :param player_action: player_action is a value (if one card is played) or a vector (if passing cards)
        :return state_data: a dictionary containing state information.
        """
        state_data = {
            'deck': self.deck,
            'actions': player_action,
            'scores': self.score
        }
        return state_data

    @property
    def card_position(self):
        """
        builds a python dictionary that lists the element position for each card on the state vector

        :return:
        """

        return {f'{v[1]}{v[0]}': i for i, v in enumerate(product(suits, cards))}
