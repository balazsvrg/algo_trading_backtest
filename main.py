import datetime as dt
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web
import macd

def main():
    start = dt.datetime(2020,1,3)
    end = dt.datetime(2021,3,13)

    df = web.DataReader('TSLA', 'yahoo', start, end)
    
    plots = []
    macd.add_macd(df, plots)
    mpf.plot(df, type='candle', style='yahoo', title='TSLA', volume=True, addplot=plots)

if __name__ == "__main__":
    main()
