# Selection all
#SELECT * from agent;
#SELECT * from game;
#SELECT * from state;

#SELECT state_id FROM state ORDER by state_id DESC limit 1;
#SELECT game_id FROM game ORDER by game_id DESC limit 1;

# Retrieve the final score of games
SELECT s1.*, g1.time, g1.agent1, g1.agent2, g1.agent3, g1.agent4
FROM state s1
LEFT JOIN state s2
ON (s1.game_uuid = s2.game_uuid AND s1.state_id < s2.state_id)
LEFT JOIN  game g1
ON (s1.game_uuid = g1.game_uuid)
WHERE s2.state_id is NULL ORDER BY state_id DESC LIMIT 10;

# Shows the file size of the database
SELECT table_schema AS 'Database', SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' FROM information_schema.TABLES GROUP BY table_schema

# Packet size
#SET GLOBAL max_allowed_packet=256000000;
#SHOW variables like 'max_allowed_packet';

# 
#SHOW GRANTS FOR remote_usr
#SHOW GLOBAL STATUS;
#SHOW VARIABLES LIKE 'secure_file_priv';
# Truncate Tables
#SET FOREIGN_KEY_CHECKS=0; TRUNCATE TABLE game; ALTER TABLE game AUTO_INCREMENT=0; SET FOREIGN_KEY_CHECKS=1;
#SET FOREIGN_KEY_CHECKS=0; TRUNCATE TABLE state; ALTER TABLE state AUTO_INCREMENT=0; SET FOREIGN_KEY_CHECKS=1;