import pandas as pd
import sys
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier


run_in_dir = sys.argv[1]
walk_in_dir = sys.argv[2]

run_data = pd.read_csv(run_in_dir, parse_dates = ["time"], index_col = False)
run_data = run_data.drop(labels="Unnamed: 7", axis="columns")

walk_data = pd.read_csv(walk_in_dir, parse_dates = ["time"], index_col = False)
walk_data = walk_data.drop(labels="Unnamed: 7", axis="columns")

walk_data1 = pd.read_csv("data/participant2/walking/left_ankle/l_ankle_walk1.csv", parse_dates = ["time"], index_col = False)
walk_data1 = walk_data1.drop(labels="Unnamed: 7", axis="columns")

run_data1 = pd.read_csv("data/participant2/running/l_ankle_run.csv", parse_dates = ["time"], index_col=False)
run_data1 = run_data1.drop(labels="Unnamed: 7", axis="columns")

run_data["running"] = 1
run_data1["running"] = 1

walk_data["running"] = 0
walk_data1["running"] = 0

data = walk_data.append(run_data)
data = data.reset_index(drop=True)

data1 = walk_data1.append(run_data1)
data1 = data1.reset_index(drop=True)

# print(run_data)
# print(run_data.describe())

# print(walk_data)
# print(walk_data.describe())

# print(data)
# print(data.describe())

X = data.filter(["ax", "ay", "az", "wx", "wy", "wz"])
y = data["running"]

X1 = data1.filter(["ax", "ay", "az", "wx", "wy", "wz"])
y1 = data1["running"]

X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, train_size = 0.5, random_state = 9293)

# model = RandomForestClassifier(n_estimators=100, random_state=1)

# model.fit(X_train, y_train)

# print(model.score(X_test, y_test))
# print(model.score(X1, y1))

print(data1)
print(data1.describe())



# print(acceleration_data)
# print(acceleration_data.describe())

# print(new)
# print(new.describe())