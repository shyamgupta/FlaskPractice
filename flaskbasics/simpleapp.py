from flask import Flask,redirect,request,flash,session,render_template
import re

app = Flask(__name__)
app.secret_key = "HelloWorld"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():
	errorCount =0
	if len(request.form['email'])<1:
		errorCount +=1
		flash('Email address cannot be blank')
	if not EMAIL_REGEX.match(request.form['email']):
		errorCount +=1
		flash('Invalid email address')
	if len(request.form['first_name'])<1:
		errorCount +=1
		flash('First name cannot be blank')
	if any(char.isdigit() for char in request.form['first_name']):
		errorCount +=1
		flash('First Name cannot be alpha numeric')
	if len(request.form['last_name'])<1:
		errorCount +=1
		flash('Last name cannot be blank')
	if any(char.isdigit() for char in request.form['last_name']):
		errorCount +=1
		flash('Last Name cannot be alpha numeric')
	if len(request.form['password'])<1:
		errorCount +=1
		flash('Password cannot be blank')
	if len(request.form['password'])>8:
		errorCount +=1
		flash('Please select a password less than 8 characters')
	if request.form['password'] != request.form['confirm_password']:
		errorCount +=1
		flash('Passwords do not match.')
	if errorCount == 0:
		flash('Thanks for submitting your information.')
		return redirect('/')
	else:
		return redirect('/')
	
	
	


app.run(debug=True)

