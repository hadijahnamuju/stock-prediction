import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model
import matplotlib.pyplot as pyplot
from matplotlib import style
import alpha_vantage
from alpha_vantage.timeseries import TimeSeries

#unique api key from alphavantage website
API_key = 'JUGN3829CA68IKGU'

#list of stock companies in DOW 30
symbols = ["WMT", "TSLA", "BA", "AAPL"]

stock_sheets = ["WMT.xlsx", "TSLA.xlsx", "BA.xlsx", "AAPL.xlsx"]

ts = TimeSeries(key='API_key', output_format='pandas')
j = 1

while j==1:
    for i in range (len(symbols)):
        data, meta_data = ts.get_intraday(symbol=symbols[i], interval='1min', outputsize='full')
        print(data)
        data.to_excel(stock_sheets[i])
        close_data = data['4. close']
        percent_change = close_data.pct_change()
        percent_change.to_csv("pctchange.text")
        lastval_change = percent_change[-1]

    i = i+1


stock_csv = ['WMT.csv', 'TSLA.csv', 'BA.csv', 'AAPL.csv']


for i in range (len(stock_csv)):
    data = pd.read_csv(stock_csv[i])
    data = data[["1. open", "2. high", "3. low", "4. close", "5. volume"]]
    print(data.head())

    predict = "4. close"

    x = np.array(data.drop([predict], 1))
    y = np.array(data[predict])
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)


    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    acc = linear.score(x_test, y_test)
    print(acc)


    print('Coefficient: ', linear.coef_)
    print('Intercept: ', linear.intercept_)

    predictions = linear.predict(x_test)

    for x in range(len(predictions)):
        print(predictions[x], x_test[x], y_test[x])


    p = '1. open'
    style.use("ggplot")
    pyplot.scatter(data[p], data["4. close"])
    pyplot.xlabel(p)
    pyplot.ylabel("4. close")
    pyplot.show()

