import datetime as dt
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web

def main():
    start = dt.datetime(2021,3,3)
    end = dt.datetime(2021,3,13)

    df = web.DataReader('TSLA', 'yahoo', start, end)
    df.drop(['Volume', 'Adj Close'], axis=1)

    print(df.head())

    mpf.plot(df, type='candle', style='yahoo', title='AAPL', mav=(26,12), volume=True)

if __name__ == "__main__":
    main()

#test commit to solve name conflict (i hate people who said naming a branch master is racist...)