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
Create the necessary directories (from within the scratch directory if on ARGO or the same directory the container .sif or .simg container image is in) needed by MySQL:
<br></br>
`mkdir -p ${PWD}/mysql/var/lib/mysql ${PWD}/mysql/run/mysqld`


Start the singularity instance of the mysql container:
<br></br>
`singularity instance start -e -c --bind ${PWD}/mysql/var/lib/mysql/:/var/lib/mysql --bind ${PWD}/mysql/run/mysqld:/run/mysqld mysql_latest.sif mysql_container`

Next run the instance, this command runs the the MySQL server program, mysqld in the container:
<br></br>
`singularity run instance://mysql_container`

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

*When you stop the instance or an error occurs its best to check if the lock on the socket has been released. Delete ./mysql/run/mysqld/mysqld.sock.lock.
*You may also need to delete the instance directory in ~/.singularity/instances/sing/os/user_name/instance_name.
