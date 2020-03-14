#!/bin/bash
# Write the host of the MySQL server container to a file.
hostname > mysql_hostname

# Start instance.
singularity instance start -e -c --bind ${SCRATCH}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${SCRATCH}/mysql/run/mysqld:/run/mysqld mysql_latest.sif mysqlheart

# Run the instance.
singularity run instance://mysqlheart
