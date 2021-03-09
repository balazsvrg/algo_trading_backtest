import datetime as dt
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web
import indicators as ind

def main():
    start = dt.datetime(2020,1,3)
    end = dt.datetime(2021,3,13)

    df = web.DataReader('TSLA', 'yahoo', start, end)
    
    plots = []
    ind.add_macd(df, plots)
    ind.add_sma(df, plots, span=20)
    ind.add_ema(df, plots, span=20)
    ind.add_rsi(df, plots)
    mpf.plot(df, type='candle', style='yahoo', title='TSLA', volume=True, addplot=plots)

    ind.add_rsi(df, plots, 14)

if __name__ == "__main__":
    main()
