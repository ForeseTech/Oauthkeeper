######################
# ESCAPING FUNCTIONS #
######################

def escape_special_characters( string ):
	escapedString = ""

	for character in string:
		if character == '\'':
			escapedString += '\''
		else:
			escapedString += character
	
	return escapedString

print("\'")
