### MySQL Workbench

## Set up Database Connection
* Download MySQL Workbench.
* Once installed from the top drop down menu database, click on `Manage Connections` under the database drop down menu.
* Click on New and give the connection a name.
* Next select `connect to database` under the database drop down menu.
* Next select `Standard TCP/IP over SSH` in connection method.
* Enter `argo.orc.gmu.edu` for SSH Hostname.
* Enter user name for SSH username.
* Press Store in Vault and enter Argo login password.
* Enter hostname for MySQL Hostname. ie NODE011 This must be changed everything time for different nodes.
* Enter `remote_usr` for Username.
* Press Store in Vault and enter the randomly generated password.
![Manage Connection](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/Manage_connections.png)

## Connect to Database
* Once completed, Connect to the database.
~[Connect to database](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/connect_to_database.png)

## Import Cardiathena Database
* Select `Data Import/Restore` under the administration tab.
* Select `Import from Self-Contained File` and import cardiathena.sql.
![Import Database](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/import_database.png)
<br></br>
Under the schema tab, right click and refresh all. The database should now show up.
![Refresh databases](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/refresh_db.png)

## Import Workbench queries
* To run queries, select `Open SQL Script` under file.
* Import `workbench_queries.sql`
* To execute queries, select execute under the Query drop down menu.
![Import workbench queries](https://raw.githubusercontent.com/c-to-the-fazzy/cardiathena/mysql-on-argo/documentation/img/import_script.png)
