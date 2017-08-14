from flask import Flask,render_template,session,url_for, request,redirect
import random
import random
app = Flask(__name__)
app.secret_key = "HelloWorld"

@app.route('/' ,methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/guess',methods=['POST'])
def guess():
	if 'rand' not in session:
		session['rand'] = random.randint(1,101)
	guess = int(request.form['guess'])
	
	if guess < session['rand']:
		session['user_guess'] = 'Too Low'
	elif guess > session['rand']:
		session['user_guess'] = 'Too High'
	else:
		session['user_guess'] = 'Correct'
	return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
	session.clear()
	return redirect('/')


app.run(debug=True)
