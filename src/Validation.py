import re

def validate_number( number ):
	valid = re.match("[0-9]{10}", number)
	
	if valid:
		return True
	else:
		return False

def validate_username( username ):
	valid = re.match("^[a-zA-Z0-9]+$", username)

	if valid:
		return True
	else:
		return False

def validate_email( email ):
	valid = re.match("[a-zA-Z0-9._]+@[a-zA-Z0-9]+.[a-zA-Z]+", email)

	if valid:
		return True
	else:
		return False
