# GMU ARGO
The Argo cluster consists of 84 nodes with over 1600 CPU cores and 44 GPUs. Preinstalled software is managed by a system called environment modules. 

## Slurm
Slurm is Argo's resource manager/job scheduler. Programs that users want to run are submitted to slurm as jobs on the head node. Slurm is able to schedule the jobs to run on the nodes using a shell script.

## Parameters 
Partition: Specify priority level by length of time to run, type of node (normal or big mem (>=40GB)), and gpu.
Priority level : LoPri = up to 5 days, HiPri = up to 12 hours

## Array jobs and Parallelism
Array Job: A program is ran independently many times. Example that was given was 30000%50 = 50 jobs at a time and up to 30000 times.
<br></br>
Parallel processes: Allows multiple programs to communicate with each other through sockets. Multiple MPI libraries available.

## Storage
Two options: Home directory(on the head node) can store up to 50GB with no time limit. %SCRATCH directory available with unlimited storage however a 120 day time limit is imposed. Compute nodes, and jobs running on compute nodes, do not have permissions to write to the home directory.

## Containers
Singularity 3.3.0 containers is installed on Argo. Singularity is able to run and pull images from docker hub.


## Architecture
![Architecture](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/Distributed-Computing-Architecture.png)
