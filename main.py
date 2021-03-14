import datetime as dt
import mplfinance as mpf
import pandas as pd
import pandas_datareader.data as web
import indicators as ind
import plotter as plt

def main():
    start = dt.datetime(2019,6,3)
    end = dt.datetime(2021,3,13)

    ticker = 'OTP.BD'
    # titlestring = ticker + ': ' + str(start) + ' - ' + str(end)

    otp_data = ind.market_data(web.DataReader(ticker, 'yahoo', start, end))

    otp_data.add_sma()
    otp_data.add_ema()
    otp_data.add_macd()
    otp_data.add_rsi()
    otp_data.add_bollinger()

    print(otp_data.indicators.tail(15))
    print(otp_data.has_bollinger)
    
    # plots = []
    # ind.add_macd(df, plots)
    # ind.add_sma(df, plots, span=20)
    # ind.add_ema(df, plots, span=20)
    # ind.add_rsi(df, plots)
    # ind.add_bollinger(df, plots)
    # mpf.plot(df, type='candle', style='yahoo', title=titlestring, volume=True, addplot=plots)

if __name__ == "__main__":
    main()
