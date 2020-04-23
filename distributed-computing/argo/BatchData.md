##Instructions

Change to Scratch directory:  ` cd $SCRATCH`

Clone the project if not already done so: ` git clone https://github.com/c-to-the-fazzy/cardiathena.git`

Run git fetch `git fetch`

Checkout the batch_upload branch `git checkout batch_data`

Copy helper scripts to the scratch directory: 
<br></br>
` cp cardiathena/distributed-computing/argo/helper_scripts/clean_argo_logs.sh /scratch/$USER/`
<br></br>
Copy scripts to run the game to scratch directory: 
<br></br>
` cp cardiathena/distributed-computing/argo/argo_scripts/start_game.sh /scratch/$USER/`
<br></br>
Copy the slurm files: 
<br></br>
` cp cardiathena/distributed-computing/argo/argo_scripts/*.slurm /scratch/$USER/`
<br></br>

If you have an import issue with mysql-connector: ` pip3 install --user mysql-connector-python`

Need to edit HeartsMySQLVariables.py in cardiathena/database/mysql/hearts/:
In the dictionary CONFIG, edit user to `teamw`, password will given in chat, and edit host. Host name will change based on when server goes up.
Hostname :
<br></br>
`'password': 'password',`
<br></br>
`'host': 'NODE0XX',`

Edit slurm_script job name to something slightly different:
<br></br>
`#SBATCH --job-name=<your_job_name>`
<br></br>
Edit the email field, replace user with gmu id: 
<br></br>
`#SBATCH --mail-user=<your_username>@gmu.edu`

Run the games: ` sbatch slurm_scripti.slurm`
csv files will be generated for the game and state tables in automatically created directory mysql-files.

Once the job is completed by notification by email or by checking via ` sacct -X`
Run the upload script when the Sql server is up: 
<br></br>
` sbatch upload.slurm`
<br></br>
The csv files in mysql-files/ will automatically be moved to an archive directory archive_csv/

