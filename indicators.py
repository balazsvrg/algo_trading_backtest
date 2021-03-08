import pandas as pd
import mplfinance as mpf

def add_macd(df, plots):
    ema1 = df['Close'].ewm(span=12, adjust=False).mean()
    ema2 = df['Close'].ewm(span=25, adjust=False).mean()
    df['MACD'] =  ema1 - ema2
    df['MACD SIGNAL'] = df['MACD'].ewm(span=9, adjust=False).mean()

    plots.append(mpf.make_addplot(df['MACD'], panel=1))
    plots.append(mpf.make_addplot(df['MACD SIGNAL'], panel=1))
