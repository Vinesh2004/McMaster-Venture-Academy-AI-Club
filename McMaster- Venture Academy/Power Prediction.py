from math import sqrt
from numpy import split 
from numpy import array 
from pandas import read_csv
from matplotlib import pyplot 

from statsmodels.tsa.arima_model import ARIMA


def split_dataset(data):
  train = data[1:-328]
  test = data[-328:-6] 

  train = array(split(train, len(train)/7))
  test = array(split(test, len(test)/7))

  return train, test

def to_series(data):
    series = [week[:, 0] for week in data]

    series = array(series).flatten()
    return series 

def evaluate_model(train, test):
  history = [x for x in train]

  predictions = list() 
  for i in range(len(test)):
    yhat_sequence = arima_forecast(history)
    predictions.append(yhat_sequence)
    history.append(test[i, :])
  predictions = array(predictions)
  return predictions

def arima_forecast(history):
  series = to_series(history)
  model = ARIMA(series, order=(7,0,0))
  model_fit = model.fit(disp=False)
  yhat = model_fit.predict(len(series), len(series)+6)

  return yhat

dataset = read_csv('household_power_consumption_days.csv', header=0, infer_datetime_format=True, parse_dates=['datetime'], index_col=['datetime'])
# split into train and test
train, test = split_dataset(dataset.values)
predictions = evaluate_model(train, test)

days = ['sun', 'mon', 'tue', 'wed', 'thr', 'fri', 'sat']
pyplot.plot(days, test[11], marker='o')
pyplot.plot(days, predictions[10], marker='o')
pyplot.legend(["Actual", "Predicted"])
pyplot.show

