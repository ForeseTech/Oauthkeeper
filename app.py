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

		return "{a} and {b}".format(a=username, b=password)

#@app.route('/user-contacst

@app.route('/add')
def AddContact():
	return render_template('user-add.html')
