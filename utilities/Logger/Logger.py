import datetime

def logged_in(username):
	
	file_object = open("utilities/Logger/OauthkeeperLogs.txt", "a+")
	
	current_date = datetime.datetime.now()
	log_message = "[{DATETIME}] {USERNAME} logged in.\n".format( DATETIME=current_date, USERNAME=username )

	file_object.write(log_message);
