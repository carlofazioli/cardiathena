#!/bin/bash

singularity instance stop mysqlheart
singularity instance start -e -c --bind ${SCRATCH}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${SCRATCH}/mysql/run/mysqld:/run/mysqld mysql_latest.sif mysqlheart
singularity run instance://mysqlheart
