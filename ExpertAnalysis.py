#%%
import csv
import os
import pandas as pd
import numpy as np 
import sklearn as sk

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

Y = df["result"]
del df['result']
X = df[:]

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.33)

#%%
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

from sklearn.preprocessing import OrdinalEncoder
enc = OrdinalEncoder()
X = enc.fit_transform(X)

clf = DecisionTreeClassifier(max_depth=None, min_samples_split=2,    random_state=0)
scores = cross_val_score(clf, X, Y, cv=5)
print(scores)

#%%
