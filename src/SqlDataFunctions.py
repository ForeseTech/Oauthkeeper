from SqlConnections import connection  
import MySQLdb

####################
# INSERT FUNCTIONS #
####################

# Function which inserts given details into USERS table.
def users_insert( name, admin, username, password ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " INSERT INTO USERS VALUES ( USERID, \"{NAME}\", {ADMIN}, \"{USERNAME}\", \"{PASSWORD}\" ); ".format(NAME=name, ADMIN=admin, USERNAME=username, PASSWORD=password)

	try:
		cursor.execute(sql_query)
		conn.commit()
	except:
		conn.rollback()

	conn.close()


# Function which inserts given details into CONTACTS table.
def contacts_insert( name, company, mobile, email, address, current_user ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " INSERT INTO CONTACTS VALUES ( USERID, \"{NAME}\", \"{COMPANY}\", \"{MOBILE}\", \"{EMAIL}\", \"{ADDRESS}\", STATUS, \"{CURRENTUSER}\" ); ".format( NAME=name, COMPANY=company, MOBILE=mobile, EMAIL=email, ADDRESS=address, CURRENTUSER=current_user )

	try:
		cursor.execute(sql_query)
		conn.commit()
	except Exception as e:
		conn.rollback()
		print(e)

	conn.close()


####################
# UPDATE FUNCTIONS #
####################


# Function which updates data in the CONTACTS table.
def update_contacts( userid, name, company, mobile, email, address, status ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " UPDATE CONTACTS SET NAME=\"{NAME}\", COMPANY=\"{COMPANY}\", MOBILE=\"{MOBILE}\", EMAIL=\"{EMAIL}\", ADDRESS=\"{ADDRESS}\", STATUS=\"{STATUS}\" WHERE USERID={USERID}; ".format( NAME=name, COMPANY=company, MOBILE=mobile, EMAIL=email, ADDRESS=address, STATUS=status, USERID=userid )
	
	try:
		cursor.execute(sql_query)
		conn.commit()
	except Exception as e:
		conn.rollback()
		print(e)

	conn.close()


# Function which updates data in the USERS table.
def update_users( userid, name, admin, username, password ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " UPDATE USERS SET NAME=\"{NAME}\", ADMIN={ADMIN}, USERNAME=\"{USERNAME}\", PASSWORD=\"{PASSWORD}\" WHERE USERID={USERID};  ".format( NAME=name, ADMIN=admin, USERNAME=username, PASSWORD=password, USERID=userid )

	try:
		cursor.execute(sql_query)
		conn.commit()
	except:
		conn.rollback()
	
	conn.close()


###################
# LOGIN FUNCTIONS #
###################

# Function which validates a username/password login.
def login(username, password):
	
	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT USERNAME FROM USERS WHERE USERNAME=\"{U}\" AND PASSWORD=\"{P}\"; ".format(U=username, P=password)

	try:
		cursor.execute(sql_query)
		conn.close()
	except:
		conn.close()

	for USERNAME in cursor.fetchall():
		if USERNAME[0] == username:			
			return True

	return False


#################
# GET FUNCTIONS #
#################

# Function which gets contacts data which have been permitted to be viewed by a given user.
def get_contacts(username):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS FROM CONTACTS WHERE PERMISSIONS LIKE \"%{USER}%\";  ".format(USER=username)

	try:
		cursor.execute(sql_query)
		conn.close()
	except Exception as e:
		conn.close()
		print(e)
	
	ids = []
	names = []
	companies = []
	mobiles = []
	emails = []
	addresses = []
	statuses = []

	for USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS in cursor.fetchall():
		ids.append(USERID)
		names.append(NAME)
		companies.append(COMPANY)
		mobiles.append(MOBILE)
		emails.append(EMAIL)
		addresses.append(ADDRESS)
		statuses.append(STATUS)
	
	return zip(ids, names, companies, mobiles, emails, addresses, statuses)

# Function which gets mobile number based on the contactid.
def get_mobile_number(userid):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT MOBILE FROM CONTACTS WHERE USERID={ID}; ".format(ID=userid)

	try:
		cursor.execute(sql_query)
		conn.close()

	except Exception as e:
		conn.close()
		print(e)
	
	for MOBILE in cursor.fetchall():
		return MOBILE[0]
	
	#If nothing is gotten from the DB
	return 0

# Function which gets email based on the contactid.
def get_email(userid):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT EMAIL FROM CONTACTS WHERE USERID={ID}; ".format(ID=userid)

	try:
		cursor.execute(sql_query)
		conn.close()

	except Exception as e:
		conn.close()
		print(e)
	
	for EMAIL in cursor.fetchall():
		return EMAIL[0]
	
	#If nothing is gotten from the DB
	return ""
