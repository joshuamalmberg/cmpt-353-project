from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.ensemble import AdaBoostClassifier

import pandas as pd
import numpy as np
import sys

X_labels = ["min_ax", "min_ay", "min_az", "max_ax", "max_ay", "max_az", "avg_ax", "avg_ay", "avg_az", "left", "hand"]
y_labels = ["run"]

def train_on_extracted(filepath):
    df = pd.read_csv(filepath)
    X = df.filter(X_labels).values
    y = df["run"].ravel()
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.75, random_state = 9293)

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
    return

def main(filepath):
    train_on_extracted(filepath)


if __name__=='__main__':
    training_set_filepath = sys.argv[1]
    main(training_set_filepath)