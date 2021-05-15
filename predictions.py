import pandas as pd 

temperatures = pd.read_csv("temperature.csv", usecols = ['datetime' , 'San Francisco'])
temperatures.to_json("temperatures.json")
humidities = pd.read_csv("humidity.csv" , usecols = ['datetime' , 'San Francisco'])
humidities.to_json("humidities.json")