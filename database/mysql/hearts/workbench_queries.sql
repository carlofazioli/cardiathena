# Manual Inserts
#INSERT INTO agent (id, agent_type, version) VALUES (1, "The Random Agent", 1.0);
#INSERT INTO agent (id, agent_type, version) VALUES (2, "The Low Layer", 1.0);

# Manual Deletes
#DELETE FROM agent WHERE id = 1;
#DELETE FROM agent WHERE id = 2;game


# Selection
SELECT * from agent;
SELECT * from game;
SELECT * from state;


# Shows the file size of the database
#SELECT table_schema AS "Database", SUM(data_length + index_length) / 1024 / 1024 AS 'Size (MB)' FROM information_schema.TABLES GROUP BY table_schema

# Packet size
#SET GLOBAL max_allowed_packet=256000000;
#SHOW variables like 'max_allowed_packet';

# 
#SHOW GRANTS FOR remote_usr
#SHOW GLOBAL STATUS;
#SHOW VARIABLES LIKE 'secure_file_priv';