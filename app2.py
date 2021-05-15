from flask import Flask, jsonify

import csv
import json

import pymongo

import sys

from statsmodels.tsa.arima_model import ARIMA
import pmdarima as pm

import numpy as np

import pandas as pd 

import requests
import json

api_key = "fc3b496e7190f3f52cf759d247c9637c"
lat = "37.7272"
lon = "-123.032"
url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

app = Flask(__name__)

@app.route('/48horas')
def getTemperatures48():

    response = requests.get(url)
    data = json.loads(response.text)
    temp = []
    humidity = []

    hourly = data["hourly"]
    for entry in hourly:
        temp.append(entry["temp"])
        humidity.append(entry["humidity"])

    print(temp)
    print(humidity)

    jsonList = []

    for i in range(0,len(temp)):
        jsonList.append({"hour": i,"temperature" : temp[i], "humidity" : humidity[i]})

    print(json.dumps(jsonList, indent = 1))

    return json.dumps(jsonList, indent = 1)

@app.route('/24horas')
def getTemperatures24():

    response = requests.get(url)
    data = json.loads(response.text)
    temp = []
    humidity = []

    hourly = data["hourly"]
    for entry in hourly:
        temp.append(entry["temp"])
        humidity.append(entry["humidity"])

    print(temp)
    print(humidity)

    jsonList = []

    for i in range(0,24):
        jsonList.append({"hour": i,"temperature" : temp[i], "humidity" : humidity[i]})

    print(json.dumps(jsonList, indent = 1))

    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.pqrdu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    collection = client["Prediction24API2"]["Datos"]

    data2 = json.dumps(jsonList, indent = 1)

    data = jsonList

    dataframe = pd.DataFrame(data=data)

    dictMongo = dataframe.to_dict("registers")

    collection.insert_one({'data' : dictMongo}).inserted_id
    
    return json.dumps(jsonList, indent = 1)


if __name__ == '__main__':
    app.run(debug=True , port=8000)