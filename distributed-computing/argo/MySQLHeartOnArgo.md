## MySQL server on ARGO
These modules need to be loaded at login
<br></br>
module load singularity/3.3.0
<br></br>
module load  python/3.6.7

It might be helpful to modify .bashrc (located in the home directory) so that you don’t have to load the modules every time you log on.
Add those two lines at the end of the .bashrc file, the modules will automatically be loaded on next the login.

Clone the project to the scratch directory:
<br></br>
`cd $SCRATCH`
<br></br>
`git clone https://github.com/c-to-the-fazzy/cardiathena.git`
<br></br>

Create error and output logs directory:
<br></br>
`mkdir -p /scratch/$USER/logs_argo/out/ /scratch/$USER/logs_argo/err/`
<br></br>

Copy scripts to the scratch directory:
<br></br>
`cp $SCRATCH/cardiathena/distributed-computing/argo/helper_scripts/*.sh cardiathena/distributed-computing/argo/argo_scripts/*.sh $SCRATCH`
<br></br>

### Create a symlink to the home directory

Next we need to create a symlink from the scratch directory to the home directory. This is done so that singularity can write data to the scratch directory.
<br></br>
`cd $SCRATCH`
<br></br>
`mkdir singularity`
<br></br>
`ln -s /scratch/$USER/singularity /home/$USER/.singularity `

Check that your symlink has been created correctly
<br></br>
`ls -la /home/$USER | grep "\->"`

Continue on to the next section.

## MySQL server within singularity
Pull the the singularity image from singularity hub:
<br></br>
`singularity pull shub://davidjha/mysql`
<br></br>
Download the config files, and edit the relevant password fields in .mysqlrootpw and .my.cnf to change the root password from the default:
<br></br>
`curl https://raw.githubusercontent.com/davidjha/mysql/master/my.cnf > ${PWD}/.my.cnf`
<br></br>
`curl https://raw.githubusercontent.com/davidjha/mysql/master/mysqlrootpw > ${PWD}/.mysqlrootpw`
<br></br>
On Argo symlinks need to be created:
<br></br>
`ln -s /scratch/$USER/.my.cnf /home/$USER/.my.cnf`
<br></br>
`ln -s /scratch/$USER/.mysqlrootpw /home/$USER/.mysqlrootpw`

Create the necessary directories (from within the scratch directory if on ARGO or the same directory the container .sif or .simg container image is in) needed by MySQL:
<br></br>
`mkdir -p $SCRATCH/mysql/var/lib/mysql $SCRATCH/mysql/run/mysqld`

If on Argo run salloc, which will reserve a node:
<br></br>
`./alloc_mysql_node.sh`

*Take note of the NODE number ie NODE007

Start the singularity instance of the mysql container:
<br></br>
`./start_mysql.sh`

Press enter to input the next command.

Start and run MySQL container script to create a remote user:

Create a remote user. A random password will be generated to allow log-ins remotely. Record this password.
<br></br>
`singularity exec instance://mysql_container create_remote_admin_user.sh`

Now connections can be made to the MySQL container.

### Stop singularity instance:
To stop the singularity instance:
<br></br>
`singularity instance stop mysql_container`
<br></br>
To check running Singularity instances:
<br></br>
`singularity instance list`

*When you stop the instance or an error occurs its best to check if the lock on the socket has been released. Delete ./mysql/run/mysqld/mysqld.sock.lock
<br></br>
Run:
`./clean_singularity_instances.sh`

*You may also need to clean out logs as the logs directory can fill up pretty quickly.
Run:
`./clean_argo_logs.sh`

Continue on to the next section to connect python programs to the MySQL server.

## MySQL connector for python
mysql-connector-python is required to interact with the database.

Some required packages may need to be installed (only for local machines):
<br></br>
`sudo apt-get install python3-pip python3-distutils python3-setuptools`

### Install mysql-connector-python
<br></br>
`pip3 install mysql-connector-python`

## Running the games on Argo
Log onto Argo on another terminal.

Checkout mysql-on-argo branch:
<br></br>
`git fetch`
<br></br>
`git checkout mysql-on-argo`


Modify the connection string config in /scratch/$USER/cardiathena/database/mysql/hearts/HeartsMySQLVARIABLES.py:
Edit the password field and set the host to the name of the node. ie 'host': 'NODE007',

Download the slurm script:
<br></br>
`cp /cardiathena/distributed-computing/argo/slurm_script.slurm $SCRATCH`

Edit the slurm script as needed.

Run:
<br></br>
`sbatch slurm_script.slurm`


References:
<br></br>
https://github.com/sylabs/singularity/releases/tag/v3.3.0
<br></br>
https://golang.org/doc/
<br></br>
https://www.hpc.iastate.edu/guides/containers/mysql-server
