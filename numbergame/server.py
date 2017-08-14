from flask import Flask,render_template,session,url_for, request,redirect
import random
app = Flask(__name__)
app.secret_key = "HelloWorldHowAreYou"

@app.route('/',methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/guess',methods=['POST'])
def guess():
	
	guess = int(request.form['guess'])
	if 'number' not in session:
		session['number'] = random.randint(1,100)
	if guess < session['number']:
		session['message'] = "Too Low"
		session['color_name']='red'
	elif guess>session['number']:
		session['message'] = "Too high"
		session['color_name'] = "red"
	elif guess == session['number']:
		session['message'] = "Right number!"
		session['color_name'] = "green"
	return redirect('/')

@app.route('/reset',methods=['POST'])
def reset():
	session.clear()
	return redirect('/')


app.run(debug=True)


