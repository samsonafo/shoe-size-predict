from flask import Flask, render_template, request
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from datetime import datetime
import gspread
import pandas as pd
import pickle
import numpy as np


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# load model
model = pickle.load(open('model.pkl','rb'))

creds = ServiceAccountCredentials.from_json_keyfile_name('new.json', scope)

client = gspread.authorize(creds)

sheet = client.open("shoe-size").sheet1 

#function to get current time  
def date_now():
    now = datetime.now()
    mydate = datetime.strftime(now , '%Y-%m-%d %H:%M:%S')
    return mydate

# app
app = Flask(__name__, template_folder='templates')
# routes
@app.route('/',  methods=['GET'])
def home():
    return render_template("home1.html")

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
    height = request.form['height']
    sex_no = request.form['sex_no']
    shoe_size = request.form['shoe_size']
    date_time = date_now()
    collect = [height,sex_no,shoe_size,date_time]
    sheet.insert_row(collect, 2)
    return render_template("final.html")

@app.route('/get-data',  methods=['GET'])

def getdata():   
    return render_template("get-data.html")

@app.route('/final1',  methods=['POST'])

def final1():   
    return render_template("final1.html")

if __name__ == '__home__':
    app.run(port = 5000, debug=True)
    