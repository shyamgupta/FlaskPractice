from flask import Flask, request,render_template

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/ninja')
def ninja():
	return render_template('all_ninjas.html')

@app.route('/ninja/<ninja_color>')
def color(ninja_color):
	return render_template('ninja_color.html',ninja_color=ninja_color)
	

app.run(debug=True)