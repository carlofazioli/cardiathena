#!/bin/bash

singularity instance stop mysql_container
singularity instance start -e -c --bind ${SCRATCH}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${SCRATCH}/mysql/run/mysqld:/run/mysqld mysql_latest.sif mysql_container
singularity run instance://mysql_container
