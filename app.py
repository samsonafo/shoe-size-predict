from flask import Flask, render_template, request
from oauth2client.service_account import ServiceAccountCredentials
from sklearn.model_selection import GridSearchCV
from datetime import datetime
import gspread
import pandas as pd
import pickle
import numpy as np


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# load model
model = pickle.load(open('model.pkl','rb'))

creds = ServiceAccountCredentials.from_json_keyfile_name('shoe-size.json', scope)

client = gspread.authorize(creds)

details = client.open('shoe-size').sheet1

# app
app = Flask(__name__, template_folder='templates')
# routes
@app.route('/',  methods=['GET'])
def home():
    return render_template("home.html")

@app.route('/result',  methods=['POST'])
def predict():
    if request.method == 'POST':
        # get data and convert data into dataframe
        height = request.form['height']
        sex_no = request.form['sex_no']
        data_df = pd.DataFrame([[height,sex_no]],columns=['height','sex_no'])
        # predictions
        output = model.predict(data_df)
        result = np.int(np.round(output))
        
    # return data
    return render_template("result.html",prediction=result)
@app.route('/final', methods=['POST','GET'])
def final():
    final_data = dict(request.args)
    collect2 = list(final_data.values())
    pred.insert_row(collect2, 2)
    return render_template("final.html")

@app.route('/get-data',  methods=['GET'])

def getdata():   
    return render_template("get-data.html")

if __name__ == '__home__':
    app.run(port = 5000, debug=True)
    