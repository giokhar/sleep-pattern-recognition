from data_collection import update_data_files, import_dataframes
import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF

def main():
	# update_data_files()
	df = import_dataframes()

	X = df[["half_mins_passed","heart_rate", "calories", "mets"]]
	y = df['sleep_stage'].replace(['wake','deep','rem'],'non-light')

	# model = SVC(kernel='rbf', C=1E10, gamma='auto')
	# clf = DecisionTreeClassifier(random_state=0)
	# clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(10,), random_state=0)
	# clf = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=0)
	# clf = GaussianProcessClassifier(1.0 * RBF(1.0))
	# X1, X2, y1, y2 = train_test_split(X, y, random_state=0, train_size=0.5, test_size=0.5)
	# cross_vals = cross_val_score(clf, X, y, cv=7)
	# print(sum(cross_vals)/len(cross_vals))
	# model.fit(X1, y1)

	# y2_model = model.predict(X2)
	# print(accuracy_score(y2, y2_model))

	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=21, test_size=0.3, stratify=y)
	model = KNeighborsClassifier(n_neighbors=14)
	# model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(6,))
	model.fit(X_train, y_train)
	y_pred = model.predict(X_test)
	print(model.score(X_test, y_test))


if __name__ == '__main__':
	main()