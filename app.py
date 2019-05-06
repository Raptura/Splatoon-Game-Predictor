from flask import Flask

from joblib import dump, load
model = load('best_classifier.joblib') 


