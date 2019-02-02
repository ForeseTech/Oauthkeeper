######################
# ESCAPING FUNCTIONS #
######################

def escape_special_characters( string ):
	escapedString = ""

	for character in string:
		if character == '\'':
			escapedString += '\''
		if character == '\n':
			escapedString += ' '
		if character == '\r':
			escapedString += ' '
		else:
			escapedString += character
	
	return escapedString
