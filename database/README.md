The gameplay database should hold records of game states and player actions.  Additionally, the records should hold information on game outcomes; e.g. the final scores.  

* As detailed in the [card deck](https://github.com/c-to-the-fazzy/cardiathena/wiki/Game-Adjudicator-Class-Design-Document#card-deck) section, the location of each card at any point in time can be encoded by a 52-vector.
* Scoring information:
    * A 4-vector of current scores
    * A 4-vector of end-of-round scores
    * A 4-vector of end-of-game scores  
* There may be some game logic information required, but we need to think this through:
    * The led-suit for a trick can be inferred from cards already in the trick
    * Whether hearts have been broken can be inferred from cards already won in previous tricks
    * Basically, is there any game logic that cannot be inferred from the state of the card deck?
* There may be some history-tracking data required; for example, a [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) shared by all states from a given game
* We may with to track the players that participated in a given game
    * This would probably imply the existence of a database of players?  How would we structure this?

## Database
DBMS: MySQL

### Database Schema

![EER Diagram](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/cardiathena_eer_diagram.png)

### Tables
* `history_table`: A table that contains game state data. This includes a uuid to link state data to a game. The current state of the game (ie in the game of hearts, the location of all the cards), the action(s) taken by the agent, and scoring information for each state of the game. 

![](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/state_table.png)

* `player_table`: A table that contains the agents that participated in the game and the game_uuid to the game.

![player_table](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/player_table.png)

### Functions
* `get_connection(): cnx` Returns a MySQL connection object.
* `initialize_db()`: Creates a new database, `state_db`.
* `initialize_table()`: Creates a new tables, `history_table` and `player_table`.
* `insert_state(string: query, string: game_uuid, json: state, json: action, json:score)`: Inserts state data into the MySQL database. Game_uuid is converted into a hex string from python's uuid4(), and saved as varbinary data in the database. State(vector), action(vector/int), and score(vector) are converted into python json and saved into the database.
* `insert_players(string: query, string: game_uuid, json: players):` Game_uuid is converted into a hex string from python's uuid4(), and saved as varbinary data in the database. Players is the list of agent types that participated in the game. Players is converted into python json.
* `get_data_by_key(int: id_key) : state_data` Fetches individual states using the incrementing key.
* `get_data_by_uuid(string: game_uuid): state_data` Fetches an individual state using a game's uuid.
* `get_players_by_uuid(string: game_uuid): state_data` Fetches players using a game's uuid.
* `extract_uuid(list: game_state): uuid` Decodes binary uuid into utf-8 and returns the uuid.
* `extract_state(list: game_state): state` Decodes json into a list and returns state.
* `extract_action(list: game_state): action` Decodes json into a list and returns action(s).
* `extract_score(list: game_state): score` Decodes json into a list and returns a vector of scores.
* `extract_players(list: game_state): score` Decodes json into a list and returns a vector of players.
