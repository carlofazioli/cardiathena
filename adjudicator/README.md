# Hearts Adjudicator
Derived from [Adjudicator](https://github.com/c-to-the-fazzy/cardiathena/wiki/Game-Adjudicator-Class-Design-Document)

## Documentation

### Getters

Functions that return information about the game calculated using the state.

* `current_player(State) : int` returns which player is currently choosing a card to play. It should be able to calculate who leads when no players have played yet and it should be able to calculate who plays next when at least one player has played already.

* `trick_leader(State) : int` returns and calculates the trick leader from the encoded values from the state.

* `lead_suit(State) : list<int>` returns the suit of the trick leader.

* `cards_of_trick(State) : list<int>` returns all the currently played cards in the trick.

* `trick_winner(State) : int` returns which player is currently winning the trick. This only looks at players that have played a card in the trick to determine who has played the current highest card following suit. It needs to be able to find the leading suit to determine who has the highest card.

* `trick_number(State) : int` returns the current trick number by looking at all the cards that have already been played, dividing them by four, and then adding one. This number should range from one to thirteen.

* `is_passing(State) : boolean` returns true if the players are passing and false if they are not.

* `points(State) : list<int>` returns a list of each players points for the current round.

### Unique Functions

Functions that the adjudicator will need to enforce the rules of the games. 

* `start_game() : list<Agent>` starts by creating the list of agents by randomly choosing from available agent classes. It then deals cards to the four players, makes the first player the current player, sets trick number to zero, sets trick winner to None, sets the pass type to clockwise, and initializes the player scores as zero. It should return the list of agents so the Game Manager can use them to step the game.

* `step_game(action: Action): state` - receives an action from the agent who decided on their action for their turn. If the players are choosing cards to pass, the state should not update until all four players have made their choice at which point those four actions will be used to update the state. All players will have chosen their card to pass when the fourth agent has chosen their cards to pass and then step_game will update the state based on all the decisions by passing the cards based on the pass type. If a player plays a card and is not the last player in that trick, the state will update so that the played card is currently in play by adding twenty to the value stored at the index given by the player (range 21-24 for each player). When the last player of the trick plays their card, the state should update all the cards currently in play to go to the trick winner by setting all the values above twenty to the trick winners number plus ten (range 11-14). Afterwards, the trick winner should be set to play next. When all thirteen tricks have been played, the score should be updated, the deck reshuffled, the trick number should be reset to zero, the current player should be set to player 1 for passing, trick winner should be None, and the pass_type should be set up to be the next pass type.

* `get_state() : State` returns the state variable.

* `is_finished() : Boolean` returns true if one of the player scores has reached one hundred or greater.

* `agent_turn(State) : int, state` - determines the player whose turn it is by using the information from the state. This function masks the current state so the player can receive a form they are allowed to see. If all four players have passed their cards, the player that owns the two of clubs is found (done by using the number found in index 0 of the deck list) and they received a masked state that only allows them to play the two of clubs. Returns the number of the player that should play and the masked state they should receive.

* `update_score(State) : None` uses the points to update the score at the end of a round.

* `pass_cards(Action, int, State) : None` takes the action of a player and calculates who to pass it to by using pass_type from the passed in State. After the function knows who to pass to, it gives the proper cards to that player.

* `end_of_trick(State) : None` handles the end of a trick by finding the winner and giving them the cards from the trick.

* `new_round(State) : None` handles the end of a round by updating the score, reshuffling the deck, and changing the pass_type.


![](https://github.com/c-to-the-fazzy/cardiathena/blob/master/documentation/img/Masking_tech.jpg)

**Card passing**: The player/agent must choose 3 cards. The Adjudicator will take those cards and swap them with the appropriate exchange move after all four players have made their decision.

For CW, CCW, and straight passes, the adjudicator will handle the cards passed between the agents. Players will send the cards to pass to the adjudicator and the adjudicator will pass the cards to the correct player.



1. Clockwise (CW): player1 -> player2 -> player 3 -> player4 -> player1
2. Counter-Clockwise(CCW): player1 -> player4 -> player3 -> player2 -> player1
3. Straight: player1 <-> player 3 and player2 <-> player4
4. Keep: no passing

## Unit Testing
