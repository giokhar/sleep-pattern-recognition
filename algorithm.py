from data_collection import update_data_files, import_dataframes
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def main():
	# update_data_files()
	df = import_dataframes()

	X = df[["half_mins_passed","heart_rate"]]
	y = df['sleep_stage']

	model = SVC(kernel='rbf', C=1E10, gamma='auto')
	X1, X2, y1, y2 = train_test_split(X, y, random_state=0, train_size=0.5, test_size=0.5)
	model.fit(X1, y1)

	y2_model = model.predict(X2)
	print(accuracy_score(y2, y2_model))


if __name__ == '__main__':
	main()