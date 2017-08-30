from flask import Flask,redirect,render_template,flash,request,session,url_for
import re
from mysqlconnection import MySQLConnector

app = Flask(__name__)
app.secret_key = 'HelloWorld!'

mysql = MySQLConnector(app,'emaildb')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/success',methods=['POST'])
def success():
	EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
	if not EMAIL_REGEX.match(request.form['email']):
		flash("Please enter a valid email address.")
		return render_template('index.html')
	else:
		query = 'INSERT INTO email (address,created_at,updated_at) VALUES (:address,NOW(),NOW())'
		data = {
			'address':request.form['email']
		}
		mysql.query_db(query,data)
		flash("Email updated successfully!.")
		query = 'SELECT * FROM email'
		output = mysql.query_db(query)
		return render_template('success.html',all_emails = output)
	

app.run(debug=True)

