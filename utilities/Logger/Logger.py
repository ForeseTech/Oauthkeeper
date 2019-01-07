import datetime

def logged_in(username):
	
	file_object = open("utilities/Logger/OauthkeeperLogs.txt", "a")
	
	current_date = datetime.datetime.now()
	log_message = "[{DATETIME}] {USERNAME} logged in.\n".format( DATETIME=current_date, USERNAME=username )

	file_object.write(log_message);

def added_contact(username, hr_name, company):

	file_object = open("utilities/Logger/OauthkeeperLogs.txt", "a")

	current_date = datetime.datetime.now()
	log_message = "[{DATETIME}] {USERNAME} added {HR_NAME} ({COMPANY}) as a contact.\n".format( DATETIME=current_date, USERNAME=username, HR_NAME=hr_name, COMPANY=company )

	file_object.write(log_message)

def update_contact(username, hr_name, company):

	file_object = open("utilities/Logger/OauthkeeperLogs.txt", "a")

	current_date = datetime.datetime.now()
	log_message = "[{DATETIME}] {USERNAME} updated {HR_NAME} ({COMPANY}) in his/her contacts.\n".format( DATETIME=current_date, USERNAME=username, HR_NAME=hr_name, COMPANY=company )

	file_object.write(log_message)
