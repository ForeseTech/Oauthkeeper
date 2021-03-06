from SqlConnections import connection  
import MySQLdb


####################
# INSERT FUNCTIONS #
####################


# Function which inserts given details into USERS table.
def users_insert( name, admin, username, password, team ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " INSERT INTO USERS VALUES ( USERID, \"{NAME}\", {ADMIN}, \"{USERNAME}\", \"{PASSWORD}\", \"{TEAM}\" ); ".format(NAME=name, ADMIN=admin, USERNAME=username, PASSWORD=password, TEAM=team)

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

	sql_query = " INSERT INTO CONTACTS VALUES ( USERID, \"{NAME}\", \"{COMPANY}\", \"{MOBILE}\", \"{EMAIL}\", \"{ADDRESS}\", STATUS, HRCOUNT,  \"{CURRENTUSER}\" ); ".format( NAME=name, COMPANY=company, MOBILE=mobile, EMAIL=email, ADDRESS=address, CURRENTUSER=current_user )

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
def update_contacts( userid, name, company, mobile, email, address, status, hrcount ):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " UPDATE CONTACTS SET NAME=\"{NAME}\", COMPANY=\"{COMPANY}\", MOBILE=\"{MOBILE}\", EMAIL=\"{EMAIL}\", ADDRESS=\"{ADDRESS}\", STATUS=\"{STATUS}\", HRCOUNT=\"{HRCOUNT}\" WHERE USERID={USERID}; ".format( NAME=name, COMPANY=company, MOBILE=mobile, EMAIL=email, ADDRESS=address, STATUS=status, HRCOUNT=hrcount, USERID=userid )
	
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

	except Exception as e:
		conn.rollback()
		print(e)
	
	conn.close()


# Function which updates the permissions of a given contact.
def update_permissions( userid, permissions ):
	
	conn = connection()
	cursor = conn.cursor()

	sql_query = " UPDATE CONTACTS SET PERMISSIONS='{PERMISSIONS}' WHERE USERID={USERID}; ".format( PERMISSIONS=permissions, USERID=userid )

	try:
		cursor.execute(sql_query)
		conn.commit()

	except Exception as e:
		conn.rollback()
		print(e)
	
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

	sql_query = " SELECT USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS, HRCOUNT FROM CONTACTS WHERE PERMISSIONS LIKE \"%{USER}%\";  ".format(USER=username)

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
	hrcounts = []

	for USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS, HRCOUNT in cursor.fetchall():
		ids.append(USERID)
		names.append(NAME)
		companies.append(COMPANY)
		mobiles.append(MOBILE)
		emails.append(EMAIL)
		addresses.append(ADDRESS)
		statuses.append(STATUS)
		hrcounts.append(HRCOUNT)
	
	return zip(ids, names, companies, mobiles, emails, addresses, statuses, hrcounts)

# Function which gets all contact data.
def get_all_contacts( username=None, status=None, number=None, company=None ):
	
	sql_query = " SELECT USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS, PERMISSIONS, HRCOUNT FROM CONTACTS "
	is_none = 0

	# When there are username filters
	if username != None and username!= "Username":

		is_none += 1
		sql_query += "WHERE PERMISSIONS LIKE '%{USERNAME}%' ".format(USERNAME=username)

	# When there are status filters
	if status != None and status!= "All":

		is_none += 1
		if is_none == 1:
			sql_query += "WHERE "
		else:
			sql_query += " AND "

		sql_query += "STATUS LIKE '{STATUS}' ".format(STATUS=status)
	
	# When there are mobile number filters.
	if number != None:
		
		is_none += 1
		if is_none == 1:
			sql_query += "WHERE "
		else:
			sql_query += " AND "

		sql_query += "MOBILE LIKE '%{MOBILE}%' ".format(MOBILE=number)
	
	# When there are company name filters.
	if company != None:
		
		is_none += 1
		if is_none == 1:
			sql_query += "WHERE "
		else:
			sql_query += " AND "

		sql_query += "COMPANY LIKE \"%{COMPANY}%\" ".format(COMPANY=company)

	# We add the final semicolon.
	sql_query += ";"
	
	conn = connection()
	cursor = conn.cursor()

	try:
		cursor.execute(sql_query)
		conn.close()
	
	except Exception as e:
		conn.close()
		print(e)
	
	ids = []
	names = []
	companies = []
	numbers = []
	emails = []
	addresses = []
	statuses = []
	permissions = []
	hrcounts = []

	for USERID, NAME, COMPANY, MOBILE, EMAIL, ADDRESS, STATUS, PERMISSIONS, HRCOUNT in cursor.fetchall():
		ids.append(USERID)
		names.append(NAME)
		companies.append(COMPANY)
		numbers.append(MOBILE)
		emails.append(EMAIL)
		addresses.append(ADDRESS)
		statuses.append(STATUS)
		permissions.append(PERMISSIONS)
		hrcounts.append(HRCOUNT)
	
	return zip(ids, names, companies, numbers, emails, addresses, statuses, permissions, hrcounts)

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

# We get permissions based on the user or we return all the permissions.
def get_permissions(usernames):

	conn = connection()
	cursor = conn.cursor()

	if len(usernames) == 0:
		sql_query = " SELECT USERID, NAME, COMPANY, PERMISSIONS FROM CONTACTS ORDER BY COMPANY ASC; "
	
	try:
		cursor.execute(sql_query)
		conn.close()
	
	except Exception as e:
		conn.close()
		print(e)
	
	ids = []
	names = []
	companies = []
	permissions = []

	for USERID, NAME, COMPANY, PERMISSIONS in cursor.fetchall():
		ids.append(USERID)
		names.append(NAME)
		companies.append(COMPANY)
		permissions.append(PERMISSIONS)
	
	return zip(ids, names, companies, permissions)
		

# Function to get all the usernames in the database. By default, the functions does not return admins.
def get_usernames( admins=True, second_years=True ):
	
	conn = connection()
	cursor = conn.cursor()

	if admins == False and second_years == True:
		sql_query = " SELECT USERNAME FROM USERS WHERE ADMIN&1=0 ORDER BY USERNAME; "
	elif admins == True and second_years == False:
		sql_query = " SELECT USERNAME FROM USERS WHERE ADMIN&1=1 ORDER BY USERNAME; "
	else:
		sql_query = " SELECT USERNAME FROM USERS ORDER BY USERNAME; "
	
	try:
		cursor.execute(sql_query)
		conn.close()
	
	except Exception as e:
		conn.close()
		print(e)
	
	
	usernames = []

	for USERNAME in cursor.fetchall():
		usernames.append(USERNAME[0])
	
	return usernames


# Function which gets statistics (count) of each status.
def get_statistics():

	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT STATUS, SUM(HRCOUNT) AS STATS FROM CONTACTS GROUP BY STATUS ORDER BY STATUS ASC; "

	try:
		cursor.execute(sql_query);
		conn.close()
	
	except Exception as e:
		conn.close()
		print(e)
	
	statuses = []
	statistics = []

	for STATUS, STATS in cursor.fetchall():
		statuses.append(STATUS)
		statistics.append(STATS)
	
	return zip(statuses, statistics)


# Function which gets the members of each team.
def get_team_members(ed):

	conn = connection()
	cursor = conn.cursor()

	sql_query = "SELECT USERNAME FROM USERS WHERE TEAM = \"{TEAM}\" ORDER BY USERNAME ASC; ".format(TEAM=ed)

	if ed == "All":
		sql_query = "SELECT USERNAME FROM USERS; "

	try:
		cursor.execute(sql_query)
		conn.close()
	
	except Exception as e:
		conn.close()
		print(e)
	
	members = []

	for USERNAME in cursor.fetchall():
		members.append(USERNAME[0])
	
	return members


# Function which gets all contacts handled by that particular team.
def get_all_team_contacts(ed, status=None):

	# We first get the members of each team. We then get the all the contacts of that team.

	members = get_team_members(ed)

	ids = []
	names = []
	companies = []
	numbers = []
	emails = []
	addresses = []
	statuses = []
	permissions = []
	hrcounts = []
	
	for member in members:
		
		records = get_all_contacts(member, status)

		for userid, name, company, number, email, address, this_status, permission, hrcount in records:
			ids.append(userid)
			names.append(name)
			companies.append(company)
			numbers.append(number)
			emails.append(email)
			addresses.append(address)
			statuses.append(this_status)
			permissions.append(permission)
			hrcounts.append(hrcount)

	return zip(ids, names, companies, numbers, emails, addresses, statuses, permissions, hrcounts)
				

######################
# CHECKING FUNCTIONS #
######################


# Function to check whether a user is an admin or not.
def is_admin(username):

	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT USERNAME FROM USERS WHERE ADMIN&1=1; "

	try:
		cursor.execute(sql_query)
		conn.close()

	except Exception as e:
		conn.close()
		print(e)
	
	for USERNAME in cursor.fetchall():
		if USERNAME[0] == username:
			return True
	
	return False

def is_arjun(number):

	if number == "8939227284":
		return True
	else:
		return False
