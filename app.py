import pandas as pd
from flask import Flask, jsonify, request , render_template
import pickle

# load model
model = pickle.load(open('model.pkl','rb'))

# app
app = Flask(__name__, template_folder='templates')

# routes
@app.route('/', methods=['GET'])

def home():
    return render_template("home.html")



@app.route('/result', methods=['POST'])
def predict():
    if request.method == 'POST':
        # get data
        data = request.get_json(force=True)

        # convert data into dataframe
        data.update((x, [y]) for x, y in data.items())
        data_df = pd.DataFrame.from_dict(data)

        # predictions
        result = model.predict(data_df)

        # send back to browser
        output = {'results': int(result[0])}

    # return data
    return render_template("result.html",prediction=result)

if __name__ == '__main__':
    app.run(port = 5000, debug=True)