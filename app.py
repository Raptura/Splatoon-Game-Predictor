import pandas as pd

from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])
def predict_game():

    if request.method == 'POST':
        result = request.form
        print(result)

        predict_data = transform_data(result)
        prediction = get_prediction(predict_data)
        print(prediction)

        pred_string = ""
        if prediction == 1:
            pred_string = "win"
        else:
            pred_string = "loss"

        return str(result) + "yield a prediction of: " + pred_string

    return render_template('index.html')


def transform_data(form_result):

    data_dict = {}

    data_dict["weapon_name"], data_dict["weapon_type"], data_dict["weapon_sub"], data_dict["weapon_special"] = str(form_result['weapon']).split(", ")
    
    data_dict["game_mode"] = str(form_result["game_mode"])
    data_dict["lobby_type"] = str(form_result["lobby_type"])
    data_dict["lobby_mode"] = str(form_result["lobby_mode"])
    data_dict["rank"] = str(form_result["rank"])
    data_dict["game_map"] = str(form_result["game_map"])

    data_dict["kills"] = int(form_result['kills'])
    data_dict["assists"] = int(form_result['assists'])
    data_dict["deaths"] = int(form_result['deaths'])
    data_dict["special_count"] = int(form_result['specials'])
    data_dict["turfed_ink"] = int(form_result['turfed_ink'])

    df = pd.read_csv("all_game_data.csv")


    del df['result']
    del df['game_id']
    org_X = df[:]
    print(df.head())



    pred_df = pd.Series(data_dict).to_frame().T # create the data frame
    pred_df = pred_df[df.columns] # reorder the columns
    print(pred_df)
    pred_X = pred_df[:]

    from sklearn import preprocessing

    enc = preprocessing.OrdinalEncoder()
    min_max_scaler = preprocessing.MinMaxScaler()

    org_X = enc.fit_transform(org_X)
    org_X = min_max_scaler.fit_transform(org_X)

    pred_X = enc.transform(pred_X)
    pred_X = min_max_scaler.transform(pred_X)

    return pred_X


def get_prediction(data):
    from joblib import dump, load
    from sklearn.ensemble import AdaBoostClassifier
    
    model = load('best_classifier.joblib')

    return model.predict(data)[0]


if __name__ == "__main__":
    app.run()
