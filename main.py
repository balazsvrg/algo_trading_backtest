import datetime as dt
import mplfinance as mpf
import pandas as pd
import market_data as md
import plotter as plt
import indicators as ind

def main():
    otp_data = md.market_data(pd.read_csv('data.csv'))


    otp_macd = ind.macd(otp_data)
    print(otp_macd.get_data())
    otp_macd.update(pd.read_csv('data.csv'))
    print(otp_macd.signal_at('2021-03-10'))

if __name__ == "__main__":
    main()
