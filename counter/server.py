from flask import Flask, render_template,session
app = Flask(__name__)
app.secret_key = '\x1bAp\x99\x0b\xbf\x10\xfd\x9b\x83\x0bY\xf2\x86\x92\xcbB\xe7\x98\xbd\x98\x85\xc7\x0b'
def visit_counter():
	try:
		session['counter'] += 1
	except KeyError:
		session['counter'] =1
@app.route('/')
def index():
	visit_counter()
	return render_template('index.html',counter = session['counter'])
@app.route('/bytwo',methods=['GET','POST'])
def add2():
	session['counter'] += 2
	return render_template('index.html',counter = session['counter'])

@app.route('/reset',methods=['GET','POST'])
def reset():
	session['counter'] =1
	return render_template('index.html',counter = session['counter'])

app.run(debug=True)
