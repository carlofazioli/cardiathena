# Hearts State
The state is comprised of the following components.

## Card Deck

We can record the state of all cards in the game using the following encoding.  

1. Let us settle a commonly-used ordering convention: grouping the cards by rank order `2-A` and suit order `CDSH`. 

![](https://github.com/c-to-the-fazzy/cardiathena/blob/master/documentation/img/deck_format.png) 

2. Let's also consider the possible 'locations' within a game that a given heart can be, and give an integer encoding to each location:
    * In a player hand - encoded by `1-4`
    * In a player's won tricks - encoded by `11-14`
    * Played on the table in the current trick - encoded by `21-24`
    * Lead on the table in the current trick - encoded by `31-34`

3. By placing these location encodings into a `52-`vector, we can encode the complete location state of the deck of cards.  For example, the vector `[ 13, 2, 1, 24, 31, ...]` would denote that:
    * The `2C` is in Player 3's won tricks
    * The `3C` is in Player 2's hand
    * The `4C` is in Player 1's hand
    * The `5C` is in the current trick, and was played by Player 4
    * The `6C` is the lead card of the current trick and was played by Player 1
    * etc...

4. When showing this state to an [agent](https://github.com/c-to-the-fazzy/cardiathena/wiki/Agent-Class-Design-Document), the hands of other players needs to be masked out.  We can accomplish this by adding another location encoding:
    * Hidden information - encoded by `0`
Thus, to extend the example above, when the state vector `[ 13, 2, 1, 24, 31, ...]` is shown to Player 1, the data regarding the `3C` (which is in Player 2's hand) will be 'masked out' to `0`: `[ 13, 0, 1, 24, 31, ...]`

## Scores

The state also includes the scores of the four players.  This is just a list of four `int`s.  It is updated at the end of every round.

## Pass Type

The state will keep track of the pass type for the round and whether the players are passing this trick. The pass types range from 0-3 where
  * 0 means the players are not passing
  * 1 means the players are passing clockwise
  * 2 means the players are passing counter-clockwise
  * 3 means the players are passing across
    
If pass type is negative or zero, that means players are not passing that trick. If pass type is greater than zero, players choose their cards to pass.
