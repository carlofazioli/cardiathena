#!/bin/bash

singularity instance stop mysql_container
singularity instance start -e -c --bind ${PWD}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${PWD}/mysql/run/mysqld:/run/mysqld mysql_latest.sif mysql_container
singularity run instance://mysql_container
