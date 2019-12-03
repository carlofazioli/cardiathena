#!/bin/sh

## Give your job a name to distinguish it from other jobs you run.
#SBATCH --job-name=sqltestavocado

## General partitions: all-HiPri, bigmem-HiPri   --   (12 hour limit)
##                     all-LoPri, bigmem-LoPri, gpuq  (5 days limit)
## Restricted: CDS_q, CS_q, STATS_q, HH_q, GA_q, ES_q, COS_q  (10 day limit)
#SBATCH --partition=all-HiPri

## Separate output and error messages into 2 files.
## NOTE: %u=userID, %x=jobName, %N=nodeID, %j=jobID, %A=arrayID, %a=arrayTaskID
#SBATCH --output=/scratch/%u/%x-%N-%j.out  # Output file
#SBATCH --error=/scratch/%u/%x-%N-%j.err   # Error file

## Slurm can send you updates via email
#SBATCH --mail-type=NONE         # ALL,NONE,BEGIN,END,FAIL,REQUEUE,..
#SBATCH --mail-user=dha5@gmu.edu     # Put your GMU email address here

## Specify how much memory your job needs. (2G is the default)
#SBATCH --mem=1G        # Total memory needed per task (units: K,M,G,T)
##SBATCH --cpus-per-task 2

## Specify how much time your job needs. (default: see partition above)
#SBATCH --time=0-00:20  # Total time needed for job: Days-Hours:Minutes

##SBATCH --array=1-4

## Load the relevant modules needed for the job
module load python/3.6.7
##module load singularity/2.5.1
module load singularity/3.3.0

## Run your program or script

singularity instance start -e -c -home /scratch/dha5/ --bind ${PWD}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${PWD}/mysql/run/mysqld:/run/mysqld --network-args "portmap=6603:3306/tcp" mysqlavacado.simg mysql

singularity run instance://mysql

