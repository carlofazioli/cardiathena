## Slurm
Slurm is a job scheduler/resource manager for Linux based clusters. Slurm schedules jobs to compute nodes with user defined allocation parameters such as required time, number of CPUs, amount of memory, and GPUs.

## Slurm Commands
sbatch
* Submits a job.
`sbatch script_name.slurm`

salloc
* Runs an interative session.
`salloc <slurm-parameters>`

srun
* Runs a job directly.
`srun <slurm-parameter> <your-program>`

sinfo
* Shows the status/availability of CPUs.
`sinfo -O parition, cpusstate`
or
`spart`

squeue
* Shows current and pending jobs.
`squeue`
or
`squeue -u <userID>`

sacct
* Checks status of your job.
`sacct -X`

scancel
* Cancels a job.
`scancel <jobId>`

spart
* Shows information about all the partitions.

snode
* Show information about all the nodes in the cluster.

Reference
[GMU Argo Wiki](http://wiki.orc.gmu.edu)




