import datetime as dt
import mplfinance as mpf
import pandas as pd
import plotter as plt
import indicators as ind

def main():
    otp_data = pd.read_csv('data.csv')

    indicators =    [ind.sma(otp_data), ind.ema(otp_data),
                    ind.macd(otp_data), ind.rsi(otp_data),
                    ind.bollinger(otp_data)]

    for i in indicators:
        print( i.get_type() + "-------------------------------------------------")
        print("Initial Data: ")
        print(i.get_data())
        i.update(otp_data)
        print("Data after update: ")
        print(i.get_data())
        print("Signal at 2021-03-10: ")
        print(i.signal_at('2021-03-10'))

if __name__ == "__main__":
    main()
