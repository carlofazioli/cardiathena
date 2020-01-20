from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'remote_usr',
  'password': 'VceIqmj9',
  'host': '127.0.0.1',
  'raise_on_warnings': True
}


def connect_to_database():
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    else:
        return cnx


def create_databases(mycursor, database):
    try:
        mycursor.execute("CREATE DATABASE IF NOT EXISTS " + database)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def drop_database(mycursor, database):
    try:
        mycursor.execute("DROP DATABASE " + database)
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


def show_databases(mycursor):
    mycursor.execute("SHOW DATABASES")
    for db in mycursor:
        print(db)



cnx = connect_to_database()
cursor = cnx.cursor()

create_databases(cursor, "states_db")
show_databases(cursor)
drop_database(cursor, "states_db")
show_databases(cursor)
