import sys
sys.path.insert(0, '/root/Oauthkeeper/src')
sys.path.insert(1, '/root/Oauthkeeper/utilities/logger')
sys.path.insert(2, '/root/Oauthkeeper/utilities/csv')

import SqlDataFunctions as sql
import Formatting as form
import Logger as logger
import CSVWrite as csv

from Validation import number_exists, email_exists, is_empty, validate_number, validate_email
from flask import Flask, render_template, request, flash, redirect, url_for, session, send_file

app = Flask(__name__)
app.secret_key = "8d%/?234s*&19aw}ws{"
app.config["CACHE_TYPE"] = "null"

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
@app.route('/admin/')
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
		username = request.form['username'].strip()
		password = request.form['password'].strip()

		if sql.login(username, password) == True and sql.is_admin(username) == False:
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
		username = request.form['username'].strip()
		password = request.form['password'].strip()

		if sql.login(username, password) == True and sql.is_admin(username) == True:
			session['username'] = username
			logger.logged_in(username)
			return redirect( url_for('admin_home') )
		else:
			session['error_message'] = "Invalid credentials! You shall not pass!"
			return redirect( url_for('get_admin_login') )

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect( url_for('get_login') )


@app.route('/logout-admin')
def admin_logout():
	session.pop('username')
	return redirect( url_for('get_admin_login') )



###############
# ADD CONTACT #
###############

@app.route('/add/')
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
		name = form.escape_special_characters(request.form['name']).strip()
		company = form.escape_special_characters(request.form['company']).strip()
		number = form.escape_special_characters(request.form['number']).strip()
		email = form.escape_special_characters(request.form['email']).strip()
		address = form.escape_special_characters(request.form['address']).strip()

		if is_empty(name):
			session['error_message'] = "The 'name' field is required."
		elif is_empty(company):
			session['error_message'] = "The 'company' field is required."
		elif validate_number(number) == False:
			session['error_message'] = "The mobile number is not valid."
		elif validate_email(email) == False:
			session['error_message'] = "The email address is not valid."
		elif sql.is_arjun(number):
			return redirect("http://www.arjunaravind.in")
		else:
			if number_exists(number):
				session['error_message'] = "The mobile number exists in the database."
			elif email_exists(email) and len(email.strip()) != 0:
				session['error_message'] = "The email address exists in the database."
			else:
				sql.contacts_insert( name, company, number, email, address, session['username'] )
				logger.added_contact( session['username'], name, company )
				return redirect( url_for('user_contacts', username=session['username']) )
		
		if 'error_message' in session:
			return redirect( url_for('add_contact') )

		sql.contacts_insert( name, company, number, email, address, session['username'] )
		logger.added_contact( session['username'], name, company )
		return redirect( url_for('user_contacts', username=session['username']) )

####################
# DISPLAY CONTACTS #
####################

@app.route('/<username>/')
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
		name = form.escape_special_characters(request.form['name']).strip()
		company = form.escape_special_characters(request.form['company']).strip()
		number = form.escape_special_characters(request.form['number']).strip()
		email = form.escape_special_characters(request.form['email']).strip()
		address = form.escape_special_characters(request.form['address']).strip()
		status = form.escape_special_characters(request.form['status']).strip()
		hrcount = form.escape_special_characters(request.form['hrcount']).strip()

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
				if email_exists(email) and (len(email.strip()) != 0):
					session['error_message'] = "The email address exists in the database."

			if 'error_message' in session:
				return redirect( url_for( 'user_contacts', username=session['username'] ) )

			if 'error_message' not in session:
				logger.update_contact( session['username'], name, company )

			sql.update_contacts( userid, name, company, number, email, address, status, hrcount )
			return redirect( url_for('user_contacts', username=session['username']) )

		if 'error_message' not in session:
			logger.update_contact( session['username'], name, company )

		return redirect( url_for( 'user_contacts', username=session['username'] ) )


#########
# ADMIN #
#########

# Function which renders the admin-home.html file.
@app.route('/admin/home')
@app.route('/admin/home')
def admin_home():
	if 'username' in session and sql.is_admin(session['username']):
		return render_template('admin-home.html', username=session['username'])
	else:
		return redirect( url_for('get_admin_login') )

###############
# PERMISSIONS #
###############

# Function which renders the admin-permissions.html file.
@app.route('/admin/permissions/')
@app.route('/admin/permissions')
def get_permissions():
	if 'username' in session and sql.is_admin(session['username']):
		return render_template( 'admin-permissions.html', records = sql.get_permissions([]) )
	else:
		return redirect( url_for('get_admin_login') )

@app.route('/admin/edit-permissions/<userid>', methods = ['POST'])
def edit_permissions(userid):
	if request.method == 'POST':
		permissions = request.form['permissions'].strip()

		sql.update_permissions(userid, permissions)
		logger.edited_permissions( session['username'], userid, permissions )

		return redirect( url_for('get_permissions') )

##########
# SEARCH #
##########

# Function which renders the admin-search.html file.
@app.route('/admin/search/')
@app.route('/admin/search')
def get_search():
	if 'username' in session and sql.is_admin(session['username']):
		return render_template( 'admin-search.html', usernames = sql.get_usernames(), records = sql.get_all_contacts() )
	else:
		return redirect( url_for('get_admin_login') )

# Function which gets contact data based on username and status.
@app.route('/admin/search-filter', methods = ['POST'])
def search():
	if request.method == 'POST':

		username = request.form['username']
		status = request.form['status']
		number = request.form['number']
		company = request.form['company']

		this_usernames = sql.get_usernames()
		this_records = sql.get_all_contacts( username, status, number, company )
		return render_template( 'admin-search.html', usernames = this_usernames, records = this_records )


#########
# STATS #
#########


# Function which gets statistics.
@app.route('/admin/stats')
@app.route('/admin/stats')
def get_stats():
	return render_template( 'admin-stats.html', statistics = sql.get_statistics() )


# Function which gets team statistics.
@app.route('/admin/team-statistics/')
@app.route('/admin/team-statistics')
def get_team_statistics():
	if 'username' in session and sql.is_admin(session['username']):
		return render_template( 'admin-teams.html', records = sql.get_all_team_contacts(ed = "All") )
	else:
		return redirect( url_for('get_admin_login') )

@app.route('/admin/get-team-statistics', methods = ['POST'])
def filter_team_statistics():
	if request.method == 'POST':
		ed = request.form['ed']
		status = request.form['status']

		return render_template( 'admin-teams.html', records = sql.get_all_team_contacts(ed = ed, status = status))


############
# EXCELIFY #
############


# Function which gets the excelify page.
@app.route('/admin/excelify/')
@app.route('/admin/excelify')
def get_excelify():
	return render_template( 'admin-excelify.html' )

@app.route('/admin/excelify/all-contacts.csv')
def get_all_contacts_csv():
	csv.generate_contacts()
	return send_file('/root/Oauthkeeper/static/csv/database-contacts.csv', attachment_filename='database-contacts.csv')

@app.route('/admin/excelify/confirmed-contacts.csv')
def get_confirmed_contacts_csv():
	csv.generate_contacts(status='Emailed/Confirmed')
	return send_file('/root/Oauthkeeper/static/csv/database-contacts.csv', attachment_filename='database-contacts.csv')


#############
# ADDRESSES #
#############

# Function which gets the address page.
@app.route('/admin/addresses/')
@app.route('/admin/addresses')
def get_addresses():
	return render_template( 'admin-address.html', usernames = sql.get_usernames(), records = sql.get_all_contacts() )

# Function which filters addresses based on the given form input.
@app.route('/admin/filter-addresses', methods = ['POST'])
def filter_addresses():
	if request.method == 'POST':

		username = request.form['username']
		status = request.form['status']
		number = request.form['number']
		company = request.form['company']

		this_usernames = sql.get_usernames()
		this_records = sql.get_all_contacts( username, status, number, company )
		return render_template( 'admin-address.html', usernames = this_usernames, records = this_records )

if __name__ == '__main__':
    app.run(host='0.0.0.0')
