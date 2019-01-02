from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def GetLogin():
	return render_template('user-login.html')

@app.route('/user-login', methods = ['POST'])
def ValidateUserLogin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		return "{a} and {b}".format(a=username, b=password)

@app.route('/admin-login', methods = ['POST'])
def ValidateAdminLogin():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		return "{a} and {b}".format(a=username, b=password)
