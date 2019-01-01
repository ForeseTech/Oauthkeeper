#!/usr/bin/python

#mobileArray=[]
#nameArray=[]
#emailArray=[]
  
# Simple routine to run a query on a database and print the results:
#def doQuery( conn ) :
#	cur = conn.cursor()  
#	cur.execute( "SELECT mobileNo, name, email from users where sentMail=;" )
# 
#	for mobileNo, name, email in cur.fetchall() :
#		mobileArray.append(mobileNo)
#		nameArray.append(name)
#		emailArray.append(email)


from SqlConnections import connection  
import MySQLdb

# Function which inserts given details into USERS table.
def users_insert( name, admin, username, password ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " INSERT INTO USERS VALUES ( USERID, '{NAME}', {ADMIN}, '{USERNAME}', '{PASSWORD}' ); ".format(NAME=name, ADMIN=admin, USERNAME=username, PASSWORD=password)

	try:
		cursor.execute(sql_query)
		conn.commit()
	except:
		conn.rollback()

	conn.close()


# Function which inserts given details into CONTACTS table.
def contacts_insert( name, company, mobile, email, address ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " INSERT INTO USERS VALUES ( USERID, '{NAME}', '{COMPANY}', '{MOBILE}', '{EMAIL}', '{ADDRESS}', STATUS   ".format( NAME=name, COMPANY=company, MOBILE=mobile, EMAIL=email, ADDRESS=address )

	try:
		cursor.execute(sql_query)
		conn.commit()
	except:
		conn.rollback()

	conn.close()


# Function which validates a username/password login.
def login(username, password):
	
	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT USERNAME FROM USERS WHERE USERNAME='{U}' AND PASSWORD='{P}'; ".format(U=username, P=password)

	try:
		cursor.execute(sql_query)
		conn.close()
	except:
		conn.close()

	for USERNAME in cursor.fetchall():
		if USERNAME[0] == username:			
			return True

	return False
