import pandas as pd
from flask import Flask, jsonify, request , render_template
import pickle
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime


# Connecting to google sheet api
scope = ['https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name('shoe-size-predict-406e2a882869.json', scope)

client = gspread.authorize(creds)

sheet = client.open('shoe-size-predict').sheet1



#get current time
def date_now():
    now = datetime.now()
    mydate = datetime.strftime(now , '%Y-%m-%d %H:%M:%S')
    return mydate

# load model
model = pickle.load(open('model.pkl','rb'))

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
    return render_template("final.html")

@app.route('/get-data',  methods=['POST','GET'])

def getdata():
    final_data = dict(request.args)
    collect = [date_now()]
    collect += list(final_data.values())
    sheet.insert_row(collect, 2)
    return render_template("get-data.html")

if __name__ == '__home__':
    app.run(port = 5000, debug=True)
    