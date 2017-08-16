from flask import Flask,render_template,request,redirect,flash,url_for
app = Flask(__name__)
app.config['SECRET_KEY'] = 'u\xaa9\xfa\xe5\xbbI\xc5\xef\xafXqUR\x94\xc7\x9a\x1e\xa9s[\xe3%\xec'
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
	if len(request.form['name']) <1:
		flash("Name cannot be blank!")
	else:
		flash("Success! You name is {}".format(request.form['name']))
	if len(request.form['comment'])>120:
		flash('Comments should be less than 120 characters')
	return redirect('/')

app.run(debug=True)