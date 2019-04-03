from data_collection import update_data_files, import_dataframes, get_dataframe
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

K_NEAREST_NEIGHBOR 		= KNeighborsClassifier(n_neighbors=14)
SUPPORT_VECTOR_MACHINE 	= SVC(kernel='rbf', C=1E10, gamma='auto', random_state=21)
DECISION_TREE  			= DecisionTreeClassifier(max_depth=3, random_state=21)
RANDOM_FOREST 			= RandomForestClassifier(n_estimators=100, max_depth=3, random_state=21)
NEURAL_NETWORK 			= MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(6,), random_state=7)

def get_model_score(model, days="*", binary=True):
	df = import_dataframes(days)
	X = df[["time","half_mins_passed","heart_rate", "calories", "mets"]]
	y = df['sleep_stage']
	if binary:
		y = y.replace(['wake','deep','rem'],'non-light')

	X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=21, test_size=0.3, stratify=y)
	model.fit(X_train, y_train)
	return model.score(X_test, y_test)
