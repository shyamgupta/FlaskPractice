from flask import Flask, render_template,session
app = Flask(__name__)
app.secret_key = '\x1bAp\x99\x0b\xbf\x10\xfd\x9b\x83\x0bY\xf2\x86\x92\xcbB\xe7\x98\xbd\x98\x85\xc7\x0b'
counter = 0
@app.route('/')
def index():
	counter += 1
	return render_template('index.html',counter=counter)
	

app.run(debug=True)