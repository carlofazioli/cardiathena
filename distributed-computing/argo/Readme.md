## Page Links
[Install singularity on a local linux machine](https://github.com/c-to-the-fazzy/cardiathena/wiki/Distributed-Computing-Document#installing-singularity-on-a-local-linux-machine)

[MySQL server on ARGO](https://github.com/c-to-the-fazzy/cardiathena/wiki/Distributed-Computing-Document#mysql-server-on-argo)

[MySQL server in singularity container](https://github.com/c-to-the-fazzy/cardiathena/wiki/Distributed-Computing-Document#mysql-server-within-singularity)

[MySQL connector for python](https://github.com/c-to-the-fazzy/cardiathena/wiki/Distributed-Computing-Document#mysql-connector-for-python)

[Running the games on Argo](https://github.com/c-to-the-fazzy/cardiathena/wiki/Distributed-Computing-Document#running-the-games-on-argo)


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

## Installing Singularity on a local Windows machine
Currently not recommended as Singularity is only available up to version 2.4 via Vagrant.
Argo currently does not support Singularity version 2.4.

## Installing Singularity on a local Linux machine
(Optional but can be helpful for testing, skip to [MySQL server on ARGO](https://github.com/c-to-the-fazzy/cardiathena/wiki/Distributed-Computing-Document#mysql-server-on-argo) if running only on Argo)

### Install Go

Singularity 3.3.0 requires go lang version 1.11 or above:
<br/><br/>
`wget https://dl.google.com/go/go1.13.6.linux-amd64.tar.gz`
<br></br>

Extract the tarball:
<br/><br/>
`sudo tar -C /usr/local -xzf go1.13.6.linux-amd64.tar.gz`

Add /usr/local/go/bin to the environment variable PATH:
<br/><br/>
`export PATH=$PATH:/usr/local/go/bin`

### Testing GO is installed properly
Make a workspace directory for go and set the GOPATH environment variable:
<br></br>
`mkdir go`
<br/><br/>
`go env -w GOPATH=$HOME/go`

Create a hello world program named hello.go:
<br></br>
`package main`

`import "fmt"`

`func main() {`
<br/><br/>
&nbsp;&nbsp;&nbsp;&nbsp;`fmt.Printf("hello, world\n")`
<br/><br/>
`}`

Next go to the Go workspace directory and build the hello world program:
<br></br>
`go build hello`

Run it with ./go

### Install Singularity
Download Singularity 3.3.0:
<br/><br/>
`wget https://github.com/singularityware/singularity/releases/download/v3.3.0/singularity-3.3.0.tar.gz`

Extract the tarball:
`tar xvf singularity-3.3.0.tar.gz`

Go into the extract directory:
`cd singularity`

These packages libssl and libuuid are required for this to work:
<br></br>
`sudo apt install libssl-dev uuid-dev`

Configure the singularity install with:
`./mconfig`

Now cd into builddir:
<br/><br/>
`cd builddir`
<br></br>
`make`
<br></br>
`sudo make install`

Skip to section:
[MySQL server in singularity container](https://github.com/c-to-the-fazzy/cardiathena/wiki/Distributed-Computing-Document#mysql-server-within-singularity)

## MySQL server on ARGO
These modules need to be loaded at login
<br></br>
module load singularity/3.3.0
<br></br>
module load  python/3.6.7

It might be helpful to modify .bashrc (located in the home directory) so that you don’t have to load the modules every time you log on.
Add those two lines at the end of the .bashrc file, the modules will automatically be loaded on next the login.

Create error and output logs directory:
<br></br>
`mkdir -p /scratch/$USER/logs_argo/out/`
<br></br>
`mkdir -p /scratch/$USER/logs_argo/err/`

These files are not required, but maybe helpful:
<br></br>
`wget https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/argo/argo_scripts/stop_start_mysql.sh`
<br></br>
`wget https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/argo/helper_scripts/clean_argo_logs.sh`
<br></br>
`wget https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/argo/helper_scripts/clean_singularity_instances.sh`

### Create a symlink to the home directory

Next we need to create a symlink from the scratch directory to the home directory. This is done so that singularity can write some cache data to the scratch directory.
<br></br>
`cd $SCRATCH`
<br></br>
`mkdir singularity`
<br></br>
`ln -s /scratch/$USER/singularity /home/$USER/.singularity `

Check that your symlink has been created correctly
<br></br>
`ls -la /home/$USER/.singularity | grep “\->”`

Continue on to the next section.

## MySQL server within singularity
Pull the the singularity image from singularity hub:
<br></br>
`singularity pull shub://ISU-HPC/mysql`
<br></br>
Download the config files, and edit the relevant password fields in .mysqlrootpw and .my.cnf to change the root password from the default:
<br></br>
`curl https://raw.githubusercontent.com/ISU-HPC/mysql/master/my.cnf > ${PWD}/.my.cnf`
<br></br>
`curl https://raw.githubusercontent.com/ISU-HPC/mysql/master/mysqlrootpw > ${PWD}/.mysqlrootpw`
<br></br>
On Argo symlinks need to be created:
<br></br>
`ln -s /scratch/$USER/.my.cnf /home/$USER/.my.cnf`
<br></br>
`ln -s /scratch/$USER/.mysqlrootpw /home/$USER/.mysqlrootpw`

Create the necessary directories (from within the scratch directory if on ARGO or the same directory the container .sif or .simg container image is in) needed by MySQL:
<br></br>
`mkdir -p ${PWD}/mysql/var/lib/mysql ${PWD}/mysql/run/mysqld`

If on Argo run salloc, which will reserve a node:
<br></br>
`salloc --cpus-per-task=16`

*Take note of the NODE number ie NODE007

Start the singularity instance of the mysql container:
<br></br>
`singularity instance start -e -c --bind ${PWD}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${PWD}/mysql/run/mysqld:/run/mysqld mysql_latest.sif mysql_container`


Next run the instance, this command runs the the MySQL server program, mysqld in the container:
<br></br>
`singularity run instance://mysql_container`


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
or a clean up script is available which will also clean up Argo logs
<br></br>
`wget https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/argo/clean_argo_logs.sh`

Continue on to the next section to connect python programs to the MySQL server.

## MySQL connector for python
mysql-connector-python is required to interact with the database.

Some required packages may need to be installed (only for local machines):
<br></br>
`sudo apt-get install python3-pip python3-distutils python3-setuptools`

### Install mysql-connector-python

On linux:
<br></br>
`sudo pip3 install mysql-connector-python`
<br></br>
On Argo:
<br></br>
`pip3 install mysql-connector-python`

## Running the games on Argo
Log onto Argo on another terminal.

Clone the github repository:
<br></br>
`git clone https://github.com/c-to-the-fazzy/cardiathena.git`

Checkout mysql-on-argo branch:
<br></br>
`git fetch`
<br></br>
`git checkout mysql-on-argo`


Modify the connection string config in /scratch/$USER/cardiathena/database/Connection.py:
Edit the password field and set the host to the name of the node. ie 'host': 'NODE007',

Download the slurm script:
<br></br>
`wget https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/argo/argo_scripts/slurm_script.slurm`

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
