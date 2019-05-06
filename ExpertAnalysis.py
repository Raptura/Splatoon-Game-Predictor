#%%
import csv
import os
import pandas as pd
import numpy as np 
import sklearn as sk

from sklearn import model_selection
from sklearn import preprocessing
from sklearn import ensemble
from sklearn import naive_bayes

#%%
df = pd.read_csv("all_game_data.csv")
df.head()

#%%
print("Mean Kills:", df["kills"].mean())
print("Mean Deaths: ", df["deaths"].mean())
print("Mean Turfed Ink:", df["turfed_ink"].mean())
print("Top 5 Weapons: " ,df["weapon_name"].value_counts()[:5])

#%% 
gm_group = df["game_mode"].unique()
for game_mode in gm_group:
    #print(game_mode)
    print("Top 5 Weapons in",game_mode, df[df["game_mode"] == game_mode]["weapon_name"].value_counts()[:5])
    print("Map Mode Combos", df[df["game_mode"] == game_mode]["game_map"].value_counts())

#%%

map_group = df["game_map"].unique()
for map_name in map_group:
    print("Top 5 Weapons in",map_name, df[df["game_map"] == map_name]["weapon_name"].value_counts()[:5])
    

#%%
print(df["game_mode"].value_counts())
print(df["game_map"].value_counts())

#%%

# Start with ensemble learning.

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

data = df[:]

Y = list(df["result"])
del df['result']
X = df[:]


enc = preprocessing.OrdinalEncoder()
min_max_scaler = preprocessing.MinMaxScaler()

X = enc.fit_transform(X)
X = min_max_scaler.fit_transform(X)
print(X)

for i in range(len(Y)):
    if Y[i] == "win":
        Y[i] = 1
    else:
        Y[i] = 0

print(Y)


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33)

#%%
from sklearn.tree import DecisionTreeClassifier


clf = DecisionTreeClassifier(max_depth=3)
clf.fit(X_train,y_train)
scores = model_selection.cross_val_score(clf, X_test, y_test, cv=10)
print(scores)

#%%
#Testing Gausian Naiive bayes

gnb = naive_bayes.GaussianNB()
gnb.fit(X_train, y_train)
scores = model_selection.cross_val_score(gnb, X_test, y_test, cv=10)
print(scores)


#%%
d_tree = DecisionTreeClassifier(max_depth=3)
aba = ensemble.AdaBoostClassifier(base_estimator=d_tree, n_estimators=50)

params ={
    "base_estimator__criterion": ["gini", "entropy"],
    "base_estimator__splitter": ["best", "random"]
}

cv_n = model_selection.KFold(n_splits=20, shuffle=True)
cv_search = model_selection.GridSearchCV(aba, param_grid=params, scoring="average_precision", cv=cv_n, refit=True, n_jobs=2)
cv_search.fit(X_train, y_train)
print(cv_search.score(X_test,y_test))

from joblib import dump, load
dump(cv_search.best_estimator_, 'best_classifier.joblib') 

#%%
