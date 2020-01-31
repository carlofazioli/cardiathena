#!/bin/bash

rm /scratch/$USER/mysql/run/mysqld/*.lock
rm /scratch/$USER/mysql/var/lib/mysql/*.lock
rm -r /scratch/$USER/singularity/instances/sing/*.edu
