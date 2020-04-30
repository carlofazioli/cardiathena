#!/bin/bash
# Write the host of the MySQL server container to a file.
hostname > $SCRATCH/mysql_hostname

# Start instance.
singularity instance start --userns -e -c --bind ${SCRATCH}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${SCRATCH}/mysql/run/mysqld:/run/mysqld mysql_latest.simg mysqlheart

# Run the instance.
singularity run --userns instance://mysqlheart
