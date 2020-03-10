# Low Layer Agent

`get_action(partial_state : State) : Action` creates an action with the mindset of attempting to avoid taking the trick. The low-layer plays defensively, and wants to minimize points.

## Passing
Find trouble suits by averaging the cards in each suit and choosing the highest cards from the suit with the hightest average.

## Leading
First, check if the player has any Spade cards that are Queen or higher. If they are not, they should lead with a Spades card to try and draw out the Queen of Spades.
If the Queen of Spades has already been played or the player does not have any Spades, they should choose the lowest card from one of the other suits.

## Following
If the player is not last, choose their highest card that is less than the currently highest played card. If the player is last, choose the highest safe card.

## Unique Functions
`get_action(partial_state : State) : Action` The agent will look through the played cards in the trick to see if any cards with points have been played. If there are cards with points, the player will choose a card that is lower than the current highest card if they can. The agent will randomly choose their cards when passing.

`select_card(partial_state: HeartsState):` The agent will check to see if it's leading and choose whether to play with spades in order to try and lure out the Queen. If it does not choose to lead with spades, then it will lead with a low non-spades card. If the agent is not leading, then checks are performed to see whether it is void in the suit or not. If it is not void in the suit then the agent will pick the lowest card it can, otherwise it will try and slough off high cards from trouble suits.

`is_lead(partial_state : State) : Boolean` Check if the agent should lead this current trick to properly choose an action based on that information. This function will return true when the agent should lead and will return false when the agent is following another player's lead. To accomplish this, the function will count the cards > 20 in the partial state and determine that this played is leading when the length is four. This is because the last state has finished when all four players have played and now the player needs to start the next trick.

`not_void(partial_state : State) : Boolean` Check if the agent is not void in the suit that was led for this trick. It will return true if it has any playable cards in that suit and will return false if the player is void in that suit. It will call the lead_suit function from the agents adjudicator to determine the range of the suit it should follow if it can.

`get_highest_low_card(partial_state : State) : Action` Find the card that is currently winning the trick, find all the player cards lower than that, and choose the highest one. If there are no cards that are lower than the winning card, just play an available card.

`sort_suits(partial_state: HeartsState):` All of the cards in the agents hand are sorted by suit and returned to the caller of this function.

`passing_smart_sequence(partial_state: HeartsState):` The unused passing function that represents Method 1. It passes cards from a trouble suit where the lowest card is higher than any other lowest card in any other suit. If the player becomes void, then pass off the next high cards from the next trouble suit.

`passing_smart_facevalues(partial_state: HeartsState):` The used passing function that represents Method 2. It averages the face cards in each suit, and passes the highest cards from the suit with the highest average. (J = 11, Q = 12, K = 13, A = 14). Repeat if void. 

`pick_trouble_card_suit(sorted_hands):` A helper function for `spade_lead_check(self, partial_state: HeartsState):`, it picks the suit with the least amount of cards.

`has_qs_been_played(partial_state: HeartsState):` This function will return true if the queen has been played, false otherwise.

`pick_trouble_card(sorted_hands):` This function chooses the suit with the least amount of cards and passes those starting with the highest card unimplemented so far. 

`average_suit_weight(Suit_list):` This function uses the face card values in order to calculate the average for the passed in suit.

`sloughing(partial_state: HeartsState):` This function will select the highest card it can from the trouble suit (found by `bad_suit()`)

`bad_suit():` This helper function will count the number of problem cards in each suit and return the suit with the highest number of problem cards.

`spade_lead_check(self, partial_state: HeartsState):` This function checks to see if the agent has problem cards in the Spades suit, if the agent does not, then true is returned in order to allow for the agent to play a card to try and draw out the Queen of Spades. Note that the agent will be leading with the selected card.

`lead_low_check(self, partial_state: HeartsState):` This function returns true based on whether the Queen of Spades has been played or if the agent has no spades, and false otherwise.

## Reference
[Mark's Hearts Strategies](http://mark.random-article.com/hearts/hearts_tips.pdf)
