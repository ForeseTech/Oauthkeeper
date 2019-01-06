import datetime

def logged_in(username):
	
	file_object = open("utilities/Logger/OauthkeeperLogs.txt", "w+")
	
	current_date = datetime.datetime.now()
	log_message = "[{DATETIME}] {USERNAME} logged in.".format( DATETIME=current_date, USERNAME=username )

	file_object.write(log_message);
