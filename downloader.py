import datetime as dt
import pandas as pd
import pandas_datareader.data as web

start = dt.datetime(2019,6,3)
end = dt.datetime(2021,3,13)

ticker = 'OTP.BD'

data = web.DataReader(ticker, 'yahoo', start, end)

data.to_csv('data.csv')