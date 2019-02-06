######################
# ESCAPING FUNCTIONS #
######################

def escape_special_characters( string ):
	escapedString = ""

	for character in string:
		if character == '\n':
			escapedString += ' '
		elif character == '\r':
			escapedString += ' '
		else:
			escapedString += character
	
	return escapedString
