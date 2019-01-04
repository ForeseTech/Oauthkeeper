import sys
sys.path.insert(0, '/root/Oauthkeeper/src')

from flask import Flask, render_template, request, flash
from SqlDataFunctions import login

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
			return "Invalid"
		elif is_empty(company):
			return "Invalid"
		elif validate_number(number):
			return "Invalid"
		elif validate_email(email):
			return "Invalid"
		elif is_empty(address):
			return "Invalid"
		else:
			if number_exists(number):
				return "Invalid"
			elif email_exists(number):
				return "Invalid"

		contacts_insert( name, company, number, email, address ):
		return redirect( url_for('UserLogin') )
