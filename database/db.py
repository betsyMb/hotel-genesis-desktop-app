# import the mysql client for python 

import pymysql 
	
# Create a connection object 
# IP address of the MySQL database server 
Host = "localhost"

# User name of the database server 
User = "root"	

# Password for the database user 
Password = "root"		 

conn = pymysql.connect(host=Host, user=User, password=Password) 

# Create a cursor object 
cur = conn.cursor() 

# creating database 
cur.execute("CREATE DATABASE hoteldb") 

cur.execute("SHOW DATABASES") 
databaseList = cur.fetchall() 

for database in databaseList: 
    print(database) 
	
conn.close() 
