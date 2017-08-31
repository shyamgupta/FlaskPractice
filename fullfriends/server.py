from flask import Flask,render_template,request,redirect
from mysqlconnection import MySQLConnector

app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')

# Index Page
@app.route('/')
def index():
	query = 'SELECT * FROM friends'
	friends = mysql.query_db(query)
	return render_template('index.html',all_friends=friends)

# Add Friend
@app.route('/friends',methods=['POST'])
def create():
	query = 'INSERT INTO friends (first_name,last_name,occupation) VALUES (:first_name,:last_name,:occupation)'
	context = {
		'first_name':request.form['first'],
		'last_name':request.form['last'],
		'occupation':request.form['occupation']
	}
	mysql.query_db(query,context)
	return redirect('/')

# Show edit page for a friend
@app.route('/friends/<id>/edit',methods=['GET'])
def edit(id):
	query = 'SELECT * FROM friends WHERE id = :id'
	context = {'id':id}
	friend = mysql.query_db(query,context)
	return render_template('edit.html',one_friend=friend[0])

#Update details
@app.route('/friends/<id>',methods=['POST'])
def update(id):
	query = 'UPDATE friends SET first_name=:first_name,last_name=:last_name,occupation=:occupation WHERE id=:id'
	context ={
		'first_name':request.form['first'],
		'last_name':request.form['last'],
		'occupation':request.form['occupation'],
		'id':id
	}
	mysql.query_db(query,context)
	return redirect('/')

#Delete Entry
@app.route('/friends/<id>/delete',methods=['POST'])
def destroy(id):
	query = 'DELETE FROM friends WHERE id=:id'
	context = {'id':id}
	mysql.query_db(query,context)
	return redirect('/')


app.run(debug=True)

