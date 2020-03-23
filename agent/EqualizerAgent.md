 # Equalizer Agent
`get_action(partial_state : State) : Action` creates an action with the mindset of trying to inflict as many points as possible on the other players.

## Passing
This agent passes the highest cards three cards it can from Clubs, Diamonds, Spades (excludes the queen), and finally Hearts.
## Leading
This agent leads by first attempting to void out its Clubs and Diamonds suits (whichever one is smaller.)
It does this through the function `void_out_suits(self, partial_state: HeartsState):`, which sorts
all of the suits via `sort_suits(self, partial_state: HeartsState):` and picks the suit to void accordingly. It then
chooses the lowest card from this suit it can to lead with (might actually want to start with highest card?).
## Following
This agent continues to try and void its Clubs and Diamonds suits when following 
(see function `following_suit(self, partial_state: HeartsState):`), and will play its highest card for those two suits
(if it can, see function `get_highest_safe_card(self, suit_to_choose_from: list, partial_state: HeartsState):`). 
If it is playing Spades or Hearts however, it will always try and play the lowest card it can (`get_low_card(self, suit_to_choose_from: list):`).
## Unique Functions
`is_lead(self, partial_state: HeartsState):` returns true if the agent is currently leading.

`passing(self, partial_state: HeartsState):` is the main passing function for this agent. It focuses on selecting all 
three cards out of a single suit.  It will first attempt to void out Clubs, Diamonds, Spades, and then Hearts.

`select_card(self, partial_state: HeartsState):` is the main selection routine that decides if the agent is leading or following a trick.

`void_out_suits(self, partial_state: HeartsState):` is the function that selects the suit we want to try and void, the idea is to start with voiding either Clubs
or Diamonds (whichever is shortest) followed by Hearts and then Spades.

`following_suit(self, partial_state: HeartsState):` will still attempt to void Clubs or Diamonds if it can, it may also try and play 
the highest card in its suit, if it thinks it can afford to take on potential points.

`sort_suits(self, partial_state: HeartsState):` sorts out all of the cards by suit and returns a list ordered by suit.

`have_queen(self, spades_suit: list):` if the agent has the Queen of Spades, this function will find and return it.

`played_cards_in_trick(self, partial_state: HeartsState):` gets all of the played cards in the current trick.

`get_low_card(self, suit_to_choose_from: list):` will pick the lowest card from suit_to_choose_from.

`get_highest_card(self, suit_to_choose_from: list):` will pick the highest card from suit_to_choose_from.

`get_highest_safe_card(self, suit_to_choose_from: list, partial_state: HeartsState):` will pick the safest high card from the suit the agent
needs to follow.

