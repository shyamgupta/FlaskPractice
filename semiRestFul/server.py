from flask import Flask,render_template,url_for
from mysqlconnection import MySQLConnector
app = Flask(__name__)

mysql = MySQLConnector(app,'semiRESTFul')

@app.route('/')
def index():
	query = 'SELECT id,CONCAT(first_name," ",last_name) AS "Full Name",email,DATE_FORMAT(created_at,"%M-%D-%Y") AS "Created At" FROM users'
	all_users = mysql.query_db(query)
	print all_users[0]
	return render_template('index.html' ,all_users=all_users)

app.route('/users/<id>')
def show(id):
	return render_template('index.html')

app.route('/users/<id>/edit')
def edit():
	return render_template('index.html')

app.route('/users/<id>/destroy')
def destroy():
	return render_template('index.html')

app.route('/users/new')
def new():
	return render_template('index.html')


app.run(debug=True)