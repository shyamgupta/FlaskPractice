from flask import Flask, render_template,request,redirect,session,flash,url_for
import re
from flask_bcrypt import Bcrypt
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'HelloWorld'
mysql = MySQLConnector(app,'loginreg')
bcrypt = Bcrypt(app)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
	errors = False
	if len(request.form['firstname'])<2:
		errors = True
		flash('First Name should be at least 2 characters long.')
	
	if request.form['firstname'].isalpha() == False:
		errors = True
		flash('First Name cannot have numeric characters.')
	
	if len(request.form['lastname'])<2:
		errors = True
		flash('Last Name should be at least 2 characters long.')
	
	if request.form['lastname'].isalpha() == False:
		errors = True
		flash('Last Name cannot have numeric characters.')
	
	if not EMAIL_REGEX.match(request.form['email']):
		errors = True
		flash('Invalid Email Address.')
	
	#check if email is already registered
	
	query = 'SELECT * FROM users WHERE email = :email'
	context = {'email':request.form['email']}
	if len(mysql.query_db(query,context))==1:
		errors = True
		flash('This email has already been registered.')
	
	if len(request.form['password']) <8:
		errors = True
		flash('Password should be at least 8 characters long')
	
	if request.form['password'] != request.form['cpassword']:
		errors = True
		flash('Password do not match')
	
	if errors == False:	
		pw_hash = bcrypt.generate_password_hash(request.form['password'])
		query = 'INSERT INTO users (first_name,last_name,email,pw_hash,created_at) VALUES (:first_name,:last_name,:email,:pw_hash,NOW())'
		context = {
			'first_name':request.form['firstname'],
			'last_name' : request.form['lastname'],
			'email':request.form['email'],
			'pw_hash':pw_hash,
		}
		mysql.query_db(query,context)
		flash('Your account was successfully created!')
		query='SELECT id FROM users WHERE email=:email'
		context = {'email':request.form['email']}
		session['id'] = mysql.query_db(query,context)[0]['id']
		query = 'SELECT * FROM users WHERE id=:id'
		context = {'id':session['id']}
		user = mysql.query_db(query,context)
		return render_template('success.html',one_user=user[0])
	else:
		return redirect('/')


@app.route('/login',methods=['POST'])
def login():
	#check if user exists
	query = 'SELECT * FROM users WHERE email=:email'
	context={'email':request.form['email']}
	output = mysql.query_db(query,context)
	if len(output)==0:
		flash('Incorrect Username/Password')
		return redirect('/')
	else:
		query = 'SELECT pw_hash FROM users WHERE email=:email'
		context = {'email':request.form['email']}
		user_password = mysql.query_db(query,context)
		if bcrypt.check_password_hash(user_password[0]['pw_hash'],request.form['password']):
			query='SELECT * FROM users WHERE email=:email'
			context={'email':request.form['email']}
			user = mysql.query_db(query,context)
			return render_template('success.html',one_user=user[0])
		else:
			flash('Incorrect Username/Password')
			return redirect('/')
	
@app.route('/logout',methods=['POST'])
def logout():
	session.clear()
	return redirect('/')
	


app.run(debug=True)