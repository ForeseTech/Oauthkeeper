import re
import MySQLdb
from SqlConnections import connection

######################
# VALIDATE FUNCTIONS #
#####################

# Function which validates if a number is valid or not.
def validate_number( number ):
	number = number.strip()
	valid = re.match("(^[1234567890]{10}$)|(^[1234567890]{8}$)", number)
	
	if valid:
		return True
	else:
		return False

# Function which validates if a username is valid or not.
def validate_username( username ):
	valid = re.match("^[a-zA-Z0-9]+$", username)

	if valid:
		return True
	else:
		return False

# Function which validates if an email is valid or not.
def validate_email( email ):
	email = email.strip()
	valid = re.match("[a-zA-Z0-9._]+@[a-zA-Z0-9]+(.[a-zA-Z]+)+", email)

	if valid or ( len(email) == 0 ):
		return True
	else:
		return False

def validate_department( department ):
	if department == "CSE" or department == "IT":
		return True
	elif department == "EEE" or department == "ECE":
		return True
	elif department == "MEC" or department == "AUT":
		return True
	elif department == "CIV" or department == "BIO":
		return True
	elif department == "CHE":

###################
# EXISTS FUNCTION #
###################

# Function which checks if a number already exists in the db.
def number_exists( number ):
	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT MOBILE FROM CONTACTS WHERE MOBILE='{NUMBER}'; ".format( NUMBER=number )
	
	try:
		cursor.execute(sql_query)
		conn.close()
	except:
		conn.close()
	

	for MOBILE in cursor.fetchall():
		if MOBILE[0] == number:
			return True

	return False


# Function which checks if an email already exists in the db.
def email_exists( email ):
	conn = connection()
	cursor = conn.cursor()

	sql_query = " SELECT EMAIL FROM CONTACTS WHERE EMAIL='{EMAIL}'; ".format( EMAIL=email )

	try:
		cursor.execute(sql_query)
		conn.close()
	except:
		conn.close()
	
	for EMAIL in cursor.fetchall():
		if EMAIL[0] == email:
			return True
	
	return False

###################
# EMPTY FUNCTIONS #
###################

# Function which checks whether a value is empty or not.
def is_empty( word ):
	if word:
		return False
	else:
		return True
