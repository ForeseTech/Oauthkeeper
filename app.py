import sys
sys.path.insert(0, '/root/Oauthkeeper/src')

import SqlDataFunctions as sql
import Formatting as form
from Validation import number_exists, email_exists, is_empty, validate_number, validate_email
from flask import Flask, render_template, request, flash, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "8d%/?234s*&19aw}ws{"

##################
# LOGIN & LOGOUT #
##################

@app.route('/')
def get_login():
	return render_template('user-login.html')

@app.route('/admin')
def get_admin_login():
	return render_template('admin-login.html')

@app.route('/user-login', methods = ['POST'])
def validate_user_login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if sql.login(username, password) == True:
			session['username'] = username
			return redirect( url_for('user_contacts', username=session['username']) )
		else:
			return redirect( url_for('get_login') )

@app.route('/admin-login', methods = ['POST'])
def validate_admin_login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if sql.login(username, password) == True:
			return "it is valid"
		else:
			return "it is invalid"

###############
# ADD CONTACT #
###############

@app.route('/add')
def AddContact():

	if 'username' not in session:
		return redirect( url_for('get_login') )

	return render_template('user-add.html')

@app.route('/add-contact', methods = ['POST'])
def ContactsAdd():
	if request.method == 'POST':
		name = form.escape_special_characters(request.form['name'])
		company = form.escape_special_characters(request.form['company'])
		number = form.escape_special_characters(request.form['number'])
		email = form.escape_special_characters(request.form['email'])
		address = form.escape_special_characters(request.form['address'])

		if is_empty(name):
			return "name is empty"
		elif is_empty(company):
			return "company is empty"
		elif validate_number(number) == False:
			return "number is empty"
		elif validate_email(email) == False:
			return "email is empty"
		elif is_empty(address):
			return "address is empty"
		else:
			if number_exists(number):
				return "number already exists"
			elif email_exists(email):
				return "email already exists"
			else:
				sql.contacts_insert( name, company, number, email, address )
				return redirect( url_for('get_login') )


####################
# DISPLAY CONTACTS #
####################

@app.route('/<username>')
def user_contacts(username):

	if 'username' in session:
		if session['username'] != username:
			return redirect( url_for('get_login') )
	else:
		return redirect( url_for('get_login') )

	contactRecords = sql.get_contacts(username)
	return render_template('user-contacts.html', records = contactRecords)


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
			return "name is empty"
		elif is_empty(company):
			return "company is empty"
		elif validate_number(number) == False:
			return "number is empty"
		elif validate_email(email) == False:
			return "email is empty"
		elif is_empty(address):
			return "address is empty"
		else:
			if number != sql.get_mobile_number(userid):
				if number_exists(number):
					return "number already exists"

			if email != sql.get_email(userid):
				if email_exists(email):
					return "email already exists"

			sql.update_contacts( userid, name, company, number, email, address, status )
			return redirect( url_for('get_login') )
