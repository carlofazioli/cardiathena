import random
from adjudicator.hearts_adjudicator import HeartsAdjudicator
from adjudicator.state import HeartsState
from base import Action, Agent


class HeartsAction(Action):
    """
    A Hearts action is the card index chosen by the agent
    """

    def __init__(self,
                 card_index):
        self.card_index = card_index

    def __str__(self):
        return str(self.card_index)


class LowLayer(Agent):
    """
    An random agent who selects from available legal moves.
    """

    def __init__(self):
        self.own_adj = HeartsAdjudicator()
        self.cards_in_hand = []
        self.id = 2
        self.agent_name = "The Low Layer"
        self.version = 1.0

    def __repr__(self):
        return {"id": self.id, "name": self.agent_name, "version": self.version}

    def __str__(self):
        return self.agent_name

    def get_action(self,
                   partial_state: HeartsState):
        """
        The get_action() method inspects the state for open positions and picks one randomly.
        :param partial_state: the position vector of the game.
        :return: an Action.
        """

        # Agent picks 3 cards to pass
        if partial_state.pass_type > 0:
            # three_cards = self.passing_smart_sequence(partial_state)
            three_cards = self.passing_smart_face_values(partial_state)
            return HeartsAction(three_cards)

        for i in range(len(partial_state.deck)):
            if 0 < partial_state.deck[i] < 5:
                self.cards_in_hand.append(i)

        # Agent picks a card to play
        # elif partial_state.trick_number > 0 and len(cards_in_hand) > 0:
        else:
            choice = self.select_card(partial_state)
            self.cards_in_hand = []
            return HeartsAction(choice)

    def select_card(self,
                    partial_state: HeartsState):
        # our player is leading, choosing a random card for now
        if self.spade_lead_check(partial_state):
            suits = self.sort_suits(partial_state)

        if self.is_lead(partial_state):

            if self.spade_lead_check(partial_state):  # Draw out the Queen
                suits = self.sort_suits(partial_state)
                choice = random.choice(suits[2])

            elif self.lead_low_check(partial_state):  # Play safe and play low cards
                counter = 0
                index = []
                suits = self.sort_suits(partial_state)
                for i in suits:
                    if (len(i) > 0):
                        index.append(counter)
                    counter += 1

                pre_select = random.choice(index)
                selected_suit = suits[pre_select]
                choice = selected_suit[0]
            else:
                choice = random.choice(self.cards_in_hand)
        else:
            # we're following, not leading
            if self.not_void(partial_state):
                # Not void in the leading suit
                # pick the lowest card compared to the highest currently played
                choice = self.get_highest_low_card(partial_state)
            else:
                # Void in the leading suit
                # just randomly play for now
                choice = self.sloughing(partial_state)
        return choice

    def is_lead(self,
                partial_state: HeartsState):
        """Returns true if agent is leading currently"""
        played = partial_state.deck[partial_state.deck > 20]

        if len(played) >= 4:
            return True
        return False

    def not_void(self,
                 partial_state: HeartsState):
        """Returns true if agent is not void in the leading suit"""
        lead_suit = self.own_adj.lead_suit(partial_state)
        begin = 13 * lead_suit  # beginning of range of valid cards
        end = 13 * (lead_suit + 1)  # end of range of valid cards
        for x in self.cards_in_hand:
            if begin <= x < end:
                return True
        return False

    def get_highest_low_card(self,
                             partial_state: HeartsState):
        """Find the cards that are lowest than the card currently set to win and
        choose the highest one"""
        max_card_played = self.own_adj.find_max_card(partial_state)
        max_card_player = -1
        lead_suit = self.own_adj.lead_suit(partial_state)
        begin = 13 * lead_suit  # beginning of range of valid cards
        end = 13 * (lead_suit + 1)  # end of range of valid cards
        for x in self.cards_in_hand:
            if begin <= x < end:
                if max_card_played > x > max_card_player:
                    max_card_player = x

        # TODO might need to do something other than "just play whatever and hope for the best"
        # TODO if we end up with a hand where none of the cards are less than the current max
        if max_card_player == -1:
            max_card_player = self.cards_in_hand[0]
        return max_card_player

    def sort_suits(self,
                   partial_state: HeartsState):
        """ Sort out the Cards by Suit and return a List of the suits"""
        # Clubs - Diamond - Spades - Hearts
        cards = []
        clubs = []
        Diamond = []
        spades = []
        hearts = []
        for i in range(len(partial_state.deck)):
            if 0 < partial_state.deck[i] < 5:
                cards.append(i)

        for i in range(4):
            start = i * 13
            end = start + 13
            for card in cards:
                if i == 0:
                    if start <= card < end:
                        clubs.append(card)
                elif i == 1:
                    if start <= card < end:
                        Diamond.append(card)
                elif i == 2:
                    if start <= card < end:
                        spades.append(card)
                elif i == 3:
                    if start <= card < end:
                        hearts.append(card)

        suits = [clubs, Diamond, spades, hearts]
        return suits

    def passing_smart_sequence(self, partial_state: HeartsState):
        """
        Method one passing : Pass highest cards in trouble suits: suits where the lowest
        card is higher than any other lowest card in other suits. If the player becomes void,
        then pass off the next high cards from the next trouble suit.
        """

        sorted_cards_in_hand = self.sort_suits(partial_state)
        return self.pick_trouble_card(sorted_cards_in_hand)

    def passing_smart_face_values(self,
                                 partial_state: HeartsState):
        """
        Method 2: Average the face cards in each suit, and pass the highest cards from the suit with the
        highest average. (J = 9, Q = 10, K = 11, A = 12). Repeat if void.
        """

        sorted_hands = self.sort_suits(partial_state)
        
        cards_to_pass = []

        for card in range(3):
            # Face_value_cards is a sorted by suits list of only face cards.
            face_value_cards = [[card for card in suit if 8 < (card % 13) < 13] for suit in sorted_hands]
            # Face_value_cards modulo 13 for average calculations.
            modded_face_value_cards = [self.mod_13(suit) for suit in face_value_cards]
            # Avg_face_value is a list of averaged face value cards.
            avg_face_value = [self.average_cards(suit) for suit in modded_face_value_cards]
            
            # Calculate suit_index for first check if suit is void
            highest_average = max(avg_face_value)
            suit_index = avg_face_value.index(highest_average)

            # Check if the player has any face cards to begin with
            if (avg_face_value == [0,0,0,0]):
                # There are no face cards so move on to method1 which does not rely on that
                method1 = self.pick_trouble_card(sorted_hands)
                while (len(cards_to_pass) < 3):
                    cards_to_pass.append(method1.pop(0))
                return cards_to_pass

            if sorted_hands[suit_index]:
                # Index of the highest card in sorted_hands.
                highest_card_index = len(sorted_hands[suit_index]) - 1
                # Value of the highest card in sorted_hands.
                highest_card = sorted_hands[suit_index][highest_card_index]
                # Add to cards_to_pass.
                cards_to_pass.append(highest_card)
                sorted_hands[suit_index].remove(highest_card)

        return cards_to_pass

    @staticmethod
    def average_cards(hand):
        if not hand:
            return 0
        return sum(hand) / len(hand)

    def pick_trouble_card_suit(self, sorted_hands):
        """Choose the suit with the least amount of cards
                    """

        index = -1  # Array index
        store_pos = 0
        num_cards = -1
        for suit in sorted_hands:
            index += 1
            if len(suit) > num_cards:
                num_cards = len(suit)
                store_pos = index
        return store_pos

    def has_qs_been_played(self, partial_state: HeartsState):
        """ Return True if the queen has been play and false otherwise """
        pos = 0
        for i in range(len(partial_state.deck)):
            if (partial_state.deck[i] == 36) & (partial_state.deck[i] < 20):
                return True
        return False

    def pick_trouble_card(self, sorted_hands):
        """
        Choose the suit where the lowest card is higher than the lowest card in any other suit, and pass those
        starting with the highest card. If the trouble suit becomes void, then pick the next highest card from
        the next trouble suit.

        :param sorted_hands: sort_hands is a list of lists. Each list in sorted_hands contains the cards in hand for a
        particular suit. [ C[0, 1, 4], D[13, 15], ... etc.]
        :return cards_to_pass: Cards_to_pass is a list of the 3 cards to pass following the strategy stated above.
        """

        cards_to_pass = []
        # Remove empty suits/empty lists on the off chance that an agent is void a suit at the start of the game.
        # This prevents issues with zip() and empty lists.
        if not all(sorted_hands):
            for suit in sorted_hands:
                if not suit:
                    sorted_hands.remove(suit)
        # Mod 13 each value of each suit in order to find the lo/hi cards.
        trouble_suit = [self.mod_13(suit) for suit in sorted_hands]
        for i in range(3):
            # Remove voided suits (empty lists) from sorted_hands and trouble_suit.
            # This prevents zip() issues with empty lists.
            for suit, t_suit in zip(sorted_hands, trouble_suit):
                # Suit is void, remove empty suit list from sorted_hands and trouble_suit.
                if not suit:
                    sorted_hands.remove(suit)
                    trouble_suit.remove(t_suit)
            # Stores the value of the first indices of each suit to list: lowest_cards_in_each_suit.
            lowest_cards_in_each_suit = list(zip(*trouble_suit))[0]
            # Calculate the highest card out of the lowest cards.
            lowest_high_card = max(lowest_cards_in_each_suit)
            # Get the suit index of lowest_high_card. C = 0, D = 1, S = 2, H = 3.
            suit_index = lowest_cards_in_each_suit.index(lowest_high_card)
            # Get the value of the highest card in the trouble suit.
            highest_card_in_trouble_suit = sorted_hands[suit_index].__getitem__(len(sorted_hands[suit_index]) - 1)
            cards_to_pass.append(highest_card_in_trouble_suit)
            # Remove chosen card from the lists to account for future calculations.
            sorted_hands[suit_index].__delitem__(len(sorted_hands[suit_index]) - 1)
            trouble_suit[suit_index].__delitem__(len(trouble_suit[suit_index]) - 1)
        return cards_to_pass

    @staticmethod
    def mod_13(sorted_hands):
        return [suit % 13 for suit in sorted_hands]

    def average_suit_weight(self, Suit_list):
        """ Uses the face card values in order to calculate the average """
        sum = 0
        for cards in Suit_list:
            sum += (cards % 13) + 1
        if sum == 0:
            return 0
        return sum / len(Suit_list)

    def sloughing(self,
                  partial_state: HeartsState):
        suit_to_slough = self.bad_suit()
        begin = 13 * suit_to_slough
        end = 13 * (suit_to_slough + 1)
        max_card = -1
        for cards in self.cards_in_hand:
            if begin <= cards < end and cards > max_card:
                max_card = cards
        if max_card == -1:
            max_card = self.cards_in_hand[0]
        return max_card

    def bad_suit(self):
        suit_avg = [0, 0, 0, 0]
        counter = 0
        # count up the number of problem cards per suit
        # whichever suit has more problem cards is the one we're going to slough from
        for x in range(4):
            begin = 13 * x
            end = 13 * (x + 1)
            for cards in range(begin, end):
                if cards in self.cards_in_hand:
                    suit_avg[x] += cards % 13
                    counter += 1
            if counter != 0:
                suit_avg[x] = suit_avg[x] / counter
            counter = 0

        bad_suit_index = 0
        for suit_index in range(len(suit_avg)):
            if suit_avg[suit_index] > suit_avg[bad_suit_index]:
                bad_suit_index = suit_index

        return bad_suit_index

    def spade_lead_check(self, partial_state: HeartsState):
        """not holding the QS and not in spades trouble
              (not holding KS or AS or has enough low spades to cover for the KS or AS).
              Lead with any spades to draw out the QS."""
        # Spade in the trouble suit
        suits = self.sort_suits(partial_state)
        if self.pick_trouble_card_suit(suits) == 2:
            return False

        # Spade is the trouble suit and we have to check for QS , KS , or AS
        for i in suits[2]:
            if i == 36 | i == 35 | i == 26:
                return False

        if len(suits[2]) == 0:
            return False

        return True

    def lead_low_check(self, partial_state: HeartsState):
        """Has no spades or the QS has been played, lead with the lowest card of any suit.
            Or lead with the suit that has been played the least."""
        suits = self.sort_suits(partial_state)

        # There are spades in the hand
        if (self.has_qs_been_played(partial_state)) | (len(suits[2]) == 0):
            return True

        return False
