from flask import Flask, request, redirect, render_template
from data_collection import import_dataframes

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'NO_SECRET_KEY'

@app.route('/')
def index():
	data = {}
	days = 1
	data['df'] = import_dataframes(days)
	return render_template('main.html', data=data)


if __name__ == "__main__":
	app.run(debug=True)