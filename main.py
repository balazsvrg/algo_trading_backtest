import datetime as dt
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web
import indicators as ind

def main():
    start = dt.datetime(2019,6,3)
    end = dt.datetime(2021,3,13)

    ticker = 'OTP.BD'
    titlestring = ticker + ': ' + str(start) + ' - ' + str(end)

    df = web.DataReader(ticker, 'yahoo', start, end)
    
    plots = []
    ind.add_macd(df, plots)
    ind.add_sma(df, plots, span=20)
    ind.add_ema(df, plots, span=20)
    ind.add_rsi(df, plots)
    mpf.plot(df, type='candle', style='yahoo', title=titlestring, volume=True, addplot=plots)

if __name__ == "__main__":
    main()
