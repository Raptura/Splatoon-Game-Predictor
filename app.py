from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def predict_game():

    if request.method == 'POST':
        result = request.form
        print(result)
        weapon, sub, special = result['weapon'].split("; ")
        kills = result['kills']
        assists = result['assists']
        death = result['deaths']
        specials = result['specials']
        turf = result['turfed_ink']
        game_mode = result["game_mode"]
        lobby_type = result["lobby_type"]



    return render_template('index.html')


def getPrediction(data):
    from joblib import dump, load
    from sklearn.ensemble import AdaBoostClassifier
    
    model = load('/static/best_classifier.joblib')

    return model.predict(data)


if __name__ == "__main__":
    app.run()
