#!/bin/sh
mkdir -p /scratch/$USER/logs_argo/out/ /scratch/$USER/logs_argo/err/
cp $SCRATCH/cardiathena/distributed-computing/argo/helper_scripts/*.sh cardiathena/distributed-computing/argo/argo_scripts/*.sh $SCRATCH
cp $SCRATCH/cardiathena/distributed-computing/argo/helper_scripts/*.sh cardiathena/distributed-computing/argo/helper_scripts/*.sh $SCRATCH
cd $SCRATCH
mkdir singularity
ln -s /scratch/$USER/singularity /home/$USER/.singularity
singularity pull shub://davidjha/mysql
curl https://raw.githubusercontent.com/davidjha/mysql/master/my.cnf > ${PWD}/.my.cnf
curl https://raw.githubusercontent.com/davidjha/mysql/master/mysqlrootpw > ${PWD}/.mysqlrootpw
mkdir -p $SCRATCH/mysql/var/lib/mysql $SCRATCH/mysql/run/mysqld $SCRATCH/mysql-files
