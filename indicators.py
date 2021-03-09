
import pandas as pd
import mplfinance as mpf

def add_sma(df, plots, span):
    try:
        df['SMA {}', span] = df['Close'].rolling(window=span).mean()

        plots.append(mpf.make_addplot(df['SMA {}', span]))
    except:
        print("SMA {} was not added due to an error. Check if DataFrame is correct.", span)

def add_ema(df, plots, span):
    try:
        df['EMA {}', span] = df['Close'].ewm(span=span, adjust=False).mean()

        plots.append(mpf.make_addplot(df['EMA {}', span]))
    except:
        print("EMA {} was not added due to an error. Check if DataFrame is correct.", span)

def add_macd(df, plots):
    try:
        ema1 = df['Close'].ewm(span=12, adjust=False).mean()
        ema2 = df['Close'].ewm(span=25, adjust=False).mean()
        df['MACD'] =  ema1 - ema2
        df['MACD SIGNAL'] = df['MACD'].ewm(span=9, adjust=False).mean()

        plots.append(mpf.make_addplot(df['MACD'], panel=1))
        plots.append(mpf.make_addplot(df['MACD SIGNAL'], panel=1))
    except:
        print("MACD was not added due to an error. Check if DataFrame is correct.")
