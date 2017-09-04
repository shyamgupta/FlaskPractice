from flask import Flask,render_template,url_for,redirect,flash,session,request
import re
from datetime import datetime
from mysqlconnection import MySQLConnector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'HelloWorld'
mysql = MySQLConnector(app,'thewall')
bcrypt = Bcrypt(app)

#Index page
@app.route('/')
def index():
	return render_template('index.html')

#Register User
@app.route('/register',methods=['POST'])
def register():
	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
	error = False
	if len(request.form['first_name'])<2:
		error = True
		flash('First name should be minimum 2 characters.')
	if len(request.form['last_name'])<2:
		error = True
		flash('Last name should be minimum 2 characters.')
	if not EMAIL_REGEX.match(request.form['email']):
		error=True
		flash('Please enter a valid email address')
	query = 'SELECT * FROM users WHERE email=:email'
	context = {'email':request.form['email']}
	if len(mysql.query_db(query,context)) == 1:
		error = True
		flash('This email is already registered.')
	if len(request.form['password'])<8:
		error =True
		flash('Password should be minimum 8 characters.')
	if request.form['password'] != request.form['confirm_password']:
		error=True
		flash('Passwords do not match.')
	if error == False:
		pw_hash = bcrypt.generate_password_hash(request.form['password'])
		query = 'INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) VALUES (:first_name,:last_name,:email,:password,NOW(),NOW())'
		context = {
			
			'first_name' : request.form['first_name'],
			'last_name' : request.form['last_name'],
			'email':request.form['email'],
			'password' : pw_hash
		}
		mysql.query_db(query,context)
		session['email'] = request.form['email']
		return redirect('/thewall')
	else:
		return redirect('/')

#User Login
@app.route('/login',methods=['POST'])
def login():
	#check if email is registered
	query = 'SELECT email FROM users WHERE email=:user_input'
	context = {'user_input':request.form['email']}
	if len(mysql.query_db(query,context)) <1:
		flash('Incorrect username/password')
		return redirect('/')
	else:
		query = 'SELECT password FROM users WHERE email=:user_input'
		context = {'user_input':request.form['email']}
		user_password = mysql.query_db(query,context)
		if bcrypt.check_password_hash(user_password[0]['password'],request.form['password']):
			session['email']=request.form['email']
			return redirect('/thewall')
		else:
			flash('Incorrect username/password')
			return redirect('/')
	

#Display The Wall once user logs in or signs in for the first time
@app.route('/thewall')
def thewall():
	if 'email' in session:
		#Retrieve details of logged in user
		query = 'SELECT first_name,last_name FROM users WHERE email=:email'
		context = {'email':session['email']}
		user_logged = mysql.query_db(query,context)
		#Retrieve details of ALL users
		query = 'SELECT users.id,messages.id,first_name,last_name,message,DATE_FORMAT(messages.updated_at,"%M-%d-%Y-%H:%i") AS updated_at FROM users LEFT OUTER JOIN messages ON users.id=messages.users_id ORDER BY messages.updated_at DESC'
		all_messages = mysql.query_db(query)
		print "First message {}".format(all_messages[0])
		return render_template('wall.html',all_messages=all_messages,user_logged=user_logged)
	else:
		return redirect('/')



#Post message
@app.route('/message', methods=['POST'])
def message():
	if 'email' in session:
		#retrieve users_id
		query = 'SELECT id FROM users WHERE email=:email'
		context = {'email':session['email']}
		id = mysql.query_db(query,context)
		#Insert message to 'messages' table
		query = 'INSERT INTO messages (message,created_at,updated_at,users_id) VALUES (:message,NOW(),NOW(),:id)'
		context = {'message':request.form['message'],'id':id[0]['id']}
		mysql.query_db(query,context)
		return redirect('/thewall')
	else:
		return redirect('/')

#Post comment
@app.route('/comment',methods=['POST'])
def comment():
	if 'email' in session:
		query = 'SELECT id FROM users WHERE email=:email'
		context = {'email':session['email']}
		user_id = mysql.query_db(query,context)
		query = 'INSERT into comments (users_id,messages_id,comment,created_at,updated_at) VALUES (:user_id,:message_id,:comment,NOW(),NOW())'
		context = {
			'user_id':user_id[0]['id'],
			'message_id':request.form['message_id'],
			'comment':request.form['comment']
		}
		mysql.query_db(query,context)
		return redirect('/thewall')
	else:
		return redirect('/')


#Logout
@app.route('/logout',methods=['POST'])
def logout():
	session.clear()
	return redirect('/')


app.run(debug=True)