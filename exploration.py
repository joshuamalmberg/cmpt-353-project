import pandas as pd
import numpy as np
import sys
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.ensemble import AdaBoostClassifier
from os import listdir
from os.path import isfile, join, splitext

column_names = ["time","wx","wy","wz","ax","ay","az","run","hand","left"]

df = pd.DataFrame(columns = column_names)

in_dir1 = sys.argv[1]
in_dir2 = sys.argv[2]

tot = 0

files = [f for f in listdir(in_dir1) if isfile(join(in_dir1, f))]
for file in files:
    filename, ext = splitext(file)
    print(file)
    if(ext == ".csv"):
        
        filepath = join(in_dir1, file)
        part = pd.read_csv(filepath)
        tot += part["time"].count()
        # print(part["time"].count())
        df  = df.append(part)
        print('\033[92m'+"Added "+file+'\u001b[0m')
    else:
        print('\033[91m'+file+" rejected"+'\u001b[0m')

data = df.reset_index(drop=True)
print(df)
# print(tot)

X = data.filter(["ax", "ay", "az", "wx", "wy", "wz"])
y = data["run"].astype('int') # data.filter(["run"])

X_train, X_test, y_train, y_test = train_test_split(X.values, y.values, train_size = 0.75, random_state = 9293)



nb_model = GaussianNB()
nb_model.fit(X_train, y_train)
print("Naive Bayes model score: ", nb_model.score(X_test, y_test))

kNN_model = KNeighborsClassifier(n_neighbors=10)
kNN_model.fit(X_train, y_train)
print("K Nearest Neighbours model score: ", kNN_model.score(X_test, y_test))
rf_model = RandomForestClassifier(n_estimators=100, max_depth=8)
rf_model.fit(X_train, y_train)
print("Random Forest model score: ", rf_model.score(X_test, y_test))
clf = AdaBoostClassifier(n_estimators=100, random_state=0)
clf.fit(X_train, y_train)
print("AdaBoost model score: ", clf.score(X_test, y_test))
exit()
running = data[data["run"] == 1]
walking = data[data["run"] == 0]

print(running.describe())
print(walking.describe())

running_test_size = running["time"].count()//4
walking_test_size = walking["time"].count()//4

running_train_size = running_test_size*3
walking_train_size = walking_test_size*3

data_train = running.head(running_train_size).append(walking.head(walking_train_size))
data_test = running.tail(running_test_size).append(walking.tail(walking_test_size))

data_train = data_train.sample(frac = 1).reset_index(drop=True)
data_test = data_train.sample(frac = 1).reset_index(drop=True)

data_train_X = data_train.filter(["ax", "ay", "az", "wx", "wy", "wz"]).values
data_train_y = data_train["run"].astype("int").values

X_train1, empty, y_train1, empty1 = train_test_split(data_train_X, data_train_y, train_size = 0.99, random_state = 9293)

data_test_X = data_test.filter(["ax", "ay", "az", "wx", "wy", "wz"]).values
data_test_y = data_test["run"].astype("int").values

empty, X_test1, empty, y_test1 = train_test_split(data_test_X, data_test_y, train_size = 0.01, random_state = 1000)


# X_train1 = running.head(running_train_size).filter(["ax", "ay", "az"])
# X_train1 = X_train1.append(walking.head(walking_train_size).filter(["ax", "ay", "az"]))

# y_train1 = running.head(running_train_size)["run"].astype("int")
# y_train1 = y_train1.append(walking.head(walking_train_size)["run"].astype("int"))

# X_test1 = running.tail(running_test_size).filter(["ax", "ay", "az"])
# X_test1 = X_test1.append(walking.tail(walking_test_size).filter(["ax", "ay", "az"]))

# y_test1 = running.tail(running_test_size)["run"].astype("int")
# y_test1 = y_test1.append(walking.tail(walking_test_size)["run"].astype("int"))

# print(X_train1)
# print(y_train1)

# X_train1 = X_train1.sample(frac = 1).reset_index(drop=True)
# y_train1 = y_train1.sample(frac = 1).reset_index(drop=True)

# X_test1 = X_test1.sample(frac = 1).reset_index(drop=True)
# y_test1 = y_test1.sample(frac = 1).reset_index(drop=True)

print(model.score(X_test1, y_test1))

model.fit(X_train1, y_train1)
# predicted = model.predict(X_test1.values)
# print(np.sum(predicted), np.shape(predicted))
# print(y_test1.sum(), y_test1.count())

print("Score when using first 3/4 of data set as training set and later 1/4 as testing set:", model.score(X_test1, y_test1))

df = pd.DataFrame(columns = column_names)

files = [f for f in listdir(in_dir2) if isfile(join(in_dir2, f))]
for file in files:
    filename, ext = splitext(file)
    if(ext == ".csv"):
        filepath = join(in_dir2, file)
        part = pd.read_csv(filepath)
        tot += part["time"].count()
        # print(part["time"].count())
        df  = df.append(part)
        print('\033[92m'+"Added "+file+'\u001b[0m')
    else:
        print('\033[91m'+file+" rejected"+'\u001b[0m')

data2 = df.reset_index(drop=True)

X2 = data.filter(["ax", "ay", "az", "wx", "wy", "wz"])
y2 = data["run"].astype('int') # data.filter(["run"])

empty, X2_test, empty1, y2_test = train_test_split(X2.values, y2.values, train_size = 0.01, random_state = 100120)

print(model.score(X2.values, y2.values))

