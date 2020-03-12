## General Information
[Database Document](https://github.com/c-to-the-fazzy/cardiathena/wiki/Database-Design-Document)

The gameplay database should hold records of game states and player actions.  Additionally, the records should hold information on game outcomes; e.g. the final scores.  

* As detailed in the [card deck](https://github.com/c-to-the-fazzy/cardiathena/wiki/Game-Adjudicator-Class-Design-Document#card-deck) section, the location of each card at any point in time can be encoded by a 52-vector.

* State information:
    * deck : the location of every card in the deck.see ()
    * action : the card that was selected by the agent for the trick.
    * score : the current score.
* Inferred State information:
    * The led-suit for a trick can be inferred from cards already in the trick
    * Whether hearts have been broken can be inferred from cards already won in previous tricks
    * 

## Database
DBMS: MySQL 5.7.21

### Database Schema

![EER Diagram](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/DbSchemav3.png)

### Tables
* `game_table`: A table that uses integer indices for the game id. A time stamp is also recorded to the database at the start of the game. Agent ids for the four agents participating in the game is also recorded as foreign keys. The foreign keys reference the agent table. Also recorded to the database is a uuid to uniquely identify the game.

![game_table](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/game_table.png)

* `state_table`: A table that contains game state data. This includes a uuid to link state data to a game. The current state of the game (ie in the game of hearts, the location of all the cards), the action(s) taken by the agent, and scoring information for each state of the game. 

![state_table](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/state_table.png)

* `player_table`: A table that contains the agents that participated in the game and the game_uuid to the game. Also included is the string representation of the agent type, and the version number.

![agent_table](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/player_table.png)

### Functions
* `get_connection(): cnx` Returns a MySQL connection object.
* `query_database(string: query, list: values)`: General query execution to the database. 
* `insert_state(string: file)`: File is the path to write to a .csv file. The csv file is then loaded into the database. This can be significantly faster than regular insert statements. see [load data](https://dev.mysql.com/doc/refman/5.7/en/insert-optimization.html). Inserts state data into the MySQL database. Game_uuid is converted into a hex string from python's uuid4(), and saved as varbinary data in the database.  State(vector), action(vector/int), and score(vector) are converted into python json and saved into the database.
* `get_data_by_key(int: id_key) : state_data` Fetches individual states using the incrementing key.
* `extract_uuid(list: game_state): uuid` Decodes binary uuid into utf-8 and returns the uuid.
* `extract_state(list: game_state): state` Decodes json into a list and returns state.
* `extract_action(list: game_state): action` Decodes json into a list and returns action(s).
* `extract_score(list: game_state): score` Decodes json into a list and returns a vector of scores.
* `extract_players(list: game_state): score` Decodes json into a list and returns a vector of players.
