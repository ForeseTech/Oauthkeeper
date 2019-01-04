import sys
sys.path.insert(0, '/root/Oauthkeeper/src')

from flask import Flask, render_template, request, flash
from SqlDataFunctions import login
from Validation import number_exists, email_exists, is_empty, validate_number, validate_email

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
		name = request.form['name']
		company = request.form['company']
		number = request.form['number']
		email = request.form['email']
		address = request.form['address']

		if is_empty(name):
			return "name is empty"
		elif is_empty(company):
			return "company is empty"
		elif validate_number(number):
			return "number is empty"
		elif validate_email(email):
			return "email is empty"
		elif is_empty(address):
			return "address is empty"
		else:
			if number_exists(number):
				return "number already exists"
			elif email_exists(number):
				return "email already exists"

		contacts_insert( name, company, number, email, address )
		return redirect( url_for('UserLogin') )
