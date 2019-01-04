import sys
sys.path.insert(0, "/root/Oauthkeeper/src")

import MySQLdb
from SqlConnections import connection
from SqlDataFunctions import users_insert

# Function which deletes all existing users.
def delete_existing_users():
	conn = connection()
	cursor = conn.cursor()

	sql_query = " DELETE FROM USERS; "

	try:
		cursor.execute( sql_query )
		conn.commit()

	except Exception as e:
		conn.rollback()
		print(e)
	
	conn.close()

# Function which sets auto increment property to 1.
def set_autoincrement( num ):
	conn = connection()
	cursor = conn.cursor()

	sql_query = "ALTER TABLE USERS AUTO_INCREMENT = {NUM}; ".format(NUM=num)

	try:
		cursor.execute( sql_query )
		conn.commit()

	except Exception as e:
		conn.rollback()
		print(e)
	
	conn.close()

###########################
# Program code starts here.
###########################

delete_existing_users()
set_autoincrement(1)
