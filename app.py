from flask import Flask, request, redirect, render_template
from data_collection import import_dataframes, update_data_files, get_num_days
import algorithms as alg

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'NO_SECRET_KEY'

algorithms = {
	"KNearestNeighbor"		: alg.K_NEAREST_NEIGHBOR,
	"SupportVectorMachine" 	: alg.SUPPORT_VECTOR_MACHINE,
	"DecisionTree"			: alg.DECISION_TREE,
	"RandomForest"			: alg.RANDOM_FOREST,
	"NeuralNetwork"			: alg.NEURAL_NETWORK
}
@app.route('/')
def index():
	data = {}

	data['labels'], data['values'] = [], []
	for name in algorithms.keys():
		data['labels'].append(name)
		data['values'].append(round(100 * alg.get_model_score(algorithms[name]), 2))

	return render_template('index.html', data=data)


@app.route('/algorithm/<algorithm>')
def show(algorithm):
	data = {}

	data['algorithm']  = algorithm
	data['labels'] = [i+1 for i in range(get_num_days())]
	data['values'] = []
	for day in data['labels']:
		value = round(100 * alg.get_model_score(algorithms[algorithm], days=(day)), 2)
		data['values'].append(value)

	return render_template('algorithm.html', data=data)

@app.route('/update')
def update():
	update_data_files()
	return "Updating Data Files"


if __name__ == "__main__":
	app.run(debug=True)