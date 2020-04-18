#!/bin/sh

## Give your job a name to distinguish it from other jobs you run.
#SBATCH --job-name=cardiathena

## General partitions: all-HiPri, bigmem-HiPri   --   (12 hour limit)
##                     all-LoPri, bigmem-LoPri, gpuq  (5 days limit)
## Restricted: CDS_q, CS_q, STATS_q, HH_q, GA_q, ES_q, COS_q  (10 day limit)
#SBATCH --partition=all-HiPri

## Separate output and error messages into 2 files.
## NOTE: %u=userID, %x=jobName, %N=nodeID, %j=jobID, %A=arrayID, %a=arrayTaskID
#SBATCH --output=/scratch/%u/logs_argo/out/%a-%N.out  # Output file
#SBATCH --error=/scratch/%u/logs_argo/err/%a-%N.err   # Error file

## Slurm can send you updates via email
#SBATCH --mail-type=BEGIN,END,FAIL         # ALL,NONE,BEGIN,END,FAIL,REQUEUE,..
#SBATCH --mail-user=dha5@gmu.edu     # Put your GMU email address here

## Specify how much memory your job needs. (2G is the default)
#SBATCH --mem=1G        # Total memory needed per task (units: K,M,G,T)

## Specify number of threads per task
#SBATCH --cpus-per-task 8

## Specify number of processes
##SBATCH --ntasks=32

## Specify number of nodes
##SBATCH --nodes=8

## Specify how processes will be distributed over the nodes
##SBATCH --ntasks-per-node=2

## Specify how much time your job needs. (default: see partition above)
##SBATCH --time=0-01:00  # Total time needed for job: Days-Hours:Minutes

#SBATCH --array=1-30

## Load the relevant modules needed for the job
module load python/3.6.7

## Run your program or script
$SCRATCH/cardiathena/distributed-computing/argo/argo_scripts/start_game.sh

 
