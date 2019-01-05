import sys
sys.path.insert(0, '/root/Oauthkeeper/src')

from flask import Flask, render_template, request, flash, redirect, url_for
from SqlDataFunctions import login, contacts_insert, get_contacts
from Validation import number_exists, email_exists, is_empty, validate_number, validate_email
from Formatting import escape_special_characters

app = Flask(__name__)

@app.route('/')
def GetLogin():
	return render_template('user-login.html')

@app.route('/admin')
def GetAdminLogin():
	return render_template('admin-login.html')

@app.route('/user-login', methods = ['POST'])
def ValidateUserLogin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if login(username, password) == True:
			return "it is valid"
		else:
			return "it is invalid"

@app.route('/admin-login', methods = ['POST'])
def ValidateAdminLogin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if login(username, password) == True:
			return "it is valid"
		else:
			return "it is invalid"

@app.route('/add')
def AddContact():
	return render_template('user-add.html')

@app.route('/add-contact', methods = ['POST'])
def ContactsAdd():
	if request.method == 'POST':
		name = escape_special_characters(request.form['name'])
		company = escape_special_characters(request.form['company'])
		number = escape_special_characters(request.form['number'])
		email = escape_special_characters(request.form['email'])
		address = escape_special_characters(request.form['address'])

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
			elif email_exists(number):
				return "email already exists"
			else:
				contacts_insert( name, company, number, email, address )
				return redirect( url_for('GetLogin') )

@app.route('/<username>')
def UserContacts(username):
	contactRecords = get_contacts(username)
	return render_template('user-contacts.html', records = contactRecords)
