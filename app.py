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

    model = pm.auto_arima(df['San Francisco'], start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)


    # Forecast
    n_periods = 24 # One day
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    fc = pd.DataFrame(fc).to_json()

    item_dict = json.loads(fc)

    def test_len(fc):
        print(len(item_dict['0']))
        assert len(item_dict['0']) == 24

    test_len(fc)
    print(len(item_dict['0']))

    return fc

@app.route('/48horas')
def getTemperatures48():

    df = pd.read_csv('temperature.csv', usecols = ['datetime' , 'San Francisco'])

    df =df[~df.isin([np.nan, np.inf, -np.inf]).any(1)]

    model = pm.auto_arima(df['San Francisco'], start_p=1, start_q=1,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=3, max_q=3, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=True,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=True)


    # Forecast
    n_periods = 48 # One day
    fc, confint = model.predict(n_periods=n_periods, return_conf_int=True)

    fc = pd.DataFrame(fc).to_json()

    # fc contains the forecasting for the next 24 hours.
    return fc

@app.route('/72horas')
def getTemperatures72():

    temperatures = pd.read_csv('temperature.csv', usecols = ['datetime' , 'San Francisco'])
    humidities = pd.read_csv('humidity.csv', usecols = ['datetime' , 'San Francisco'])

    humidities.rename(columns={"San Francisco" : "San Francisco2"})

    output1 = pd.merge(temperatures, humidities, 
                   on='datetime', 
                   how='inner')


    

    # fc contains the forecasting for the next 24 hours.
    return (pd.DataFrame(output1).to_json())


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

