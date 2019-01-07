import sys
sys.path.insert(0, '/root/Oauthkeeper/src')
sys.path.insert(0, '/root/Oauthkeeper/utilities/Logger')

import SqlDataFunctions as sql
import Formatting as form
import Logger as logger
from Validation import number_exists, email_exists, is_empty, validate_number, validate_email
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "8d%/?234s*&19aw}ws{"

##################
# LOGIN & LOGOUT #
##################

# Function which serves the login page.
@app.route('/')
def get_login():

	if 'error_message' in session:
		error_message = session['error_message']
		session.pop('error_message')
		return render_template( 'user-login.html', error=error_message )
	
	else:
		return render_template( 'user-login.html', error=None)

# Function which serves the admin-login page.
@app.route('/admin')
def get_admin_login():

	if 'error_message' in session:
		error_message = session['error_message']
		session.pop('error_message')
		return render_template( 'admin-login.html', error=error_message )
	
	else:
		return render_template('admin-login.html')

# Function which validates the user-login and sends errors if invalid.
@app.route('/user-login', methods = ['POST'])
def validate_user_login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if sql.login(username, password) == True:
			session['username'] = username
			logger.logged_in(username)
			return redirect( url_for('user_contacts', username=session['username']) )

		else:
			session['error_message'] = "Invalid credentials! You shall not pass!"
			return redirect( url_for('get_login') )

# Function which validates the admin-login and sends error if invalid.
@app.route('/admin-login', methods = ['POST'])
def validate_admin_login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if sql.login(username, password) == True and sql.is_admin(username) == True:
			session['username'] = username
			return redirect( url_for('admin_home') )
		else:
			session['error_message'] = "Invalid credentials! You shall not pass!"
			return redirect( url_for('get_admin_login') )

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect( url_for('get_login') )

###############
# ADD CONTACT #
###############

@app.route('/add')
def add_contact():

	if 'username' not in session:
		return redirect( url_for('get_login') )
	
	if 'error_message' in session:
		error_message = session['error_message']
		session.pop('error_message')
		return render_template( 'user-add.html', error=error_message )

	return render_template('user-add.html')

@app.route('/add-contact', methods = ['POST'])
def contact_add():
	if request.method == 'POST':
		name = form.escape_special_characters(request.form['name'])
		company = form.escape_special_characters(request.form['company'])
		number = form.escape_special_characters(request.form['number'])
		email = form.escape_special_characters(request.form['email'])
		address = form.escape_special_characters(request.form['address'])

		if is_empty(name):
			session['error_message'] = "The 'name' field is required."
		elif is_empty(company):
			session['error_message'] = "The 'company' field is required."
		elif validate_number(number) == False:
			session['error_message'] = "The mobile number is not valid."
		elif validate_email(email) == False:
			session['error_message'] = "The email address is not valid."
		else:
			if number_exists(number):
				session['error_message'] = "The mobile number exists in the database."
			elif email_exists(email):
				session['error_message'] = "The email address exists in the database."
			else:
				sql.contacts_insert( name, company, number, email, address, session['username'] )
				return redirect( url_for('user_contacts', username=session['username']) )

		return redirect( url_for('add_contact') )


####################
# DISPLAY CONTACTS #
####################

@app.route('/<username>')
def user_contacts(username):

	if 'username' in session:

		if session['username'] != username:
			return redirect( url_for('get_login') )

		elif 'error_message' in session:
			error_message = session['error_message']
			session.pop('error_message')

			contactRecords = sql.get_contacts(username)
			return render_template( 'user-contacts.html', records = contactRecords, error = error_message )

		else:
			contactRecords = sql.get_contacts(username)
			return render_template('user-contacts.html', records = contactRecords)


	if 'username' not in session:
		return redirect( url_for('get_login') )	

###################
# UPDATE CONTACTS #
###################


@app.route('/update-contacts/<int:userid>', methods = ['POST'])
def update_contact(userid):
	if request.method == 'POST':
		name = form.escape_special_characters(request.form['name'])
		company = form.escape_special_characters(request.form['company'])
		number = form.escape_special_characters(request.form['number'])
		email = form.escape_special_characters(request.form['email'])
		address = form.escape_special_characters(request.form['address'])
		status = form.escape_special_characters(request.form['status'])

		if is_empty(name):
			session['error_message'] = "The name is empty."
		elif is_empty(company):
			session['error_message'] = "The company name is empty."
		elif validate_number(number) == False:
			session['error_message'] = "The mobile number is not valid."
		elif validate_email(email) == False:
			session['error_message'] = "The email address is not valid."
		else:
			if number != sql.get_mobile_number(userid):
				if number_exists(number):
					session['error_message'] = "The mobile number exists in the database."

			if email != sql.get_email(userid):
				if email_exists(email):
					session['error_message'] = "The email address exists in the database."

			if 'error_message' in session:
				return redirect( url_for( 'user_contacts', username=session['username'] ) )

			sql.update_contacts( userid, name, company, number, email, address, status )
			return redirect( url_for('user_contacts', username=session['username']) )

		return redirect( url_for( 'user_contacts', username=session['username'] ) )


#########
# ADMIN #
#########

# Function which renders the admin-home.html file.
@app.route('/admin/home')
def admin_home():
	return render_template('admin-home.html', username=session['username'])

###############
# PERMISSIONS #
###############

# Function which renders the admin-permissions.html file.
@app.route('/admin/permissions')
def get_permissions():
	return render_template( 'admin-permissions.html', records = sql.get_permissions([]) )

@app.route('/admin/edit-permissions/<userid>', methods = ['POST'])
def edit_permissions(userid):
	if request.method == 'POST':
		permissions = request.form['permissions']
		sql.update_permissions(userid, permissions)
		return redirect( url_for('admin_home') )

##########
# SEARCH #
##########

# Function which renders the admin-search.html file.
@app.route('/admin/search')
def get_search():
	return render_template( 'admin-search.html', usernames = sql.get_usernames(), records = sql.get_all_contacts() )

# Function which gets contact data based on username and status.
@app.route('/admin/search-filter', methods = ['POST'])
def search():
	if request.method == 'POST':

		username = request.form['username']
		status = request.form['status']

		if (username == "All") and (status == "All"):
			this_usernames = sql.get_usernames()
			this_records = sql.get_all_contacts()
			return render_template( 'admin-search.html', usernames = this_usernames, records = this_records )

		elif (username != "All") and (status == "All"):
			this_usernames = sql.get_usernames()
			this_records = sql.get_all_contacts( username = username)
			return render_template( 'admin-search.html', usernames = this_usernames, records = this_records )

		elif (username == "All") and (status != "All"):
			this_usernames = sql.get_usernames()
			this_records = sql.get_all_contacts( status = status )
			return render_template( 'admin-search.html', usernames = this_usernames, records = this_records )

		elif (username != "All") and (status != "All"):
			this_usernames = sql.get_usernames()
			this_records = sql.get_all_contacts( username = username, status = status )
			return render_template( 'admin-search.html', usernames = this_usernames, records = this_records )
