from flask import Flask, jsonify

import unittest

import pymongo

import pytest

import sys

import json

from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm

import numpy as np

import pandas as pd 

app = Flask(__name__)


@app.route('/24horas')
def getTemperatures24():

    df = pd.read_csv('temperature.csv', usecols = ['datetime' , 'San Francisco'])

    df =df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]

    #model = pm.auto_arima(df['San Francisco'], start_p=1, start_q=1,
    #                  test='adf',       # use adftest to find optimal 'd'
    #                  max_p=3, max_q=3, # maximum p and q
    #                  m=1,              # frequency of series
    #                  d=None,           # let model determine 'd'
    #                  seasonal=False,   # No Seasonality
    #                  start_P=0, 
    #                  D=0, 
    #                  trace=True,
    #                  error_action='ignore',  
    #                  suppress_warnings=True, 
    #                  stepwise=True)


    # Forecast
    #n_periods = 24 # One day
    #fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    #fc = pd.DataFrame(fc).to_json()

    #item_dict = json.loads(fc)

    data = pd.read_json('prediction24.json')

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.pqrdu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    print(data)

    collection = client["Prediction24API2"]["Datos1"]

    dataframe = pd.DataFrame(data=data)

    dictMongo = dataframe.to_dict("registers")

    collection.insert_one({'data' : dictMongo}).inserted_id


    ret = pd.DataFrame(data).to_json()

    return ret

@app.route('/48horas')
def getTemperatures48():
    data = pd.read_json('prediction48.json')
    ret = pd.DataFrame(data).to_json()

    # fc contains the forecasting for the next 24 hours.
    return data

@app.route('/horas')
def getTemperatur():

    tem = pd.read_json('prediction72temp.json')
    hum = pd.read_json('predictionhum72.json')


    temp = []
    humidity = []

    hum2 = json.loads(hum.to_json())
    tem2 = json.loads(tem.to_json())

    hum2 = hum2["0"]
    tem2 = tem2["0"]
    for i in hum2:
        temp.append(tem2[i])
        humidity.append(hum2[i])


    print(temp)
    print(humidity)

    jsonList = []

    for i in range(0,72):
        jsonList.append({"hour": i,"temperature" : temp[i], "humidity" : humidity[i]})

    
    #fin = json.dumps(jsonList, indent = 1)

    with open('prediction72.json', 'w') as outfile:
        json.dump(jsonList, outfile)

    #return item_dict

@app.route('/72horas')
def getTemperatures72():
    data = pd.read_json('prediction72.json')
    ret = pd.DataFrame(data).to_json()
    ret2 = jsonify(ret)

    # fc contains the forecasting for the next 24 hours.
    return ret2

@app.route('/humidities')
def getHumidities():
    return pd.DataFrame(humidities).to_json()

@app.route('/predictions/24horas')
def getPredictions24():
    return jsonify(predictions)

@app.route('/predictions/48horas')
def getPredictions48():
    return jsonify(predictions)


@app.route('/predictions/72horas')
def getPredictions72():
    return jsonify(predictions)


if __name__ == '__main__':
    app.run(debug=True , port=8000)
    unittest.main()

