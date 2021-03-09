import numpy as np
import pandas as pd
import mplfinance as mpf

def add_sma(df, plots, span):
    try:
        df['SMA {}', span] = df['Close'].rolling(window=span).mean()

        # Plotting ########################################
        plots.append(mpf.make_addplot(df['SMA {}', span]))
        ###################################################
    except:
        print("SMA {} was not added due to an error. Check if DataFrame is correct.", span)

def add_ema(df, plots, span):
    try:
        df['EMA {}', span] = df['Close'].ewm(span=span, adjust=False).mean()

        # Plotting ########################################
        plots.append(mpf.make_addplot(df['EMA {}', span]))
        ###################################################
    except:
        print("EMA {} was not added due to an error. Check if DataFrame is correct.", span)

def add_macd(df, plots):
    try:
        ema1 = df['Close'].ewm(span=12, adjust=False).mean()
        ema2 = df['Close'].ewm(span=25, adjust=False).mean()
        df['MACD'] =  ema1 - ema2
        df['MACD SIGNAL'] = df['MACD'].ewm(span=9, adjust=False).mean()

        # Plotting ########################################
        plots.append(mpf.make_addplot(df['MACD'], panel=1))
        plots.append(mpf.make_addplot(df['MACD SIGNAL'], panel=1))
        ###################################################

    except:
        print("MACD was not added due to an error. Check if DataFrame is correct.")

def add_rsi(df, plots, span = 14):
    try:
        close_data = []

        for row in df.itertuples():
            close_data.append(row[4])

        # Where do I put 0-s??? it distorts the statistic both ways
        # Does it even count in data this big?
        # leaving the first 0 out for now and putting them in up_diffs later
        up_diffs = []
        down_diffs = []

        avg_updiff = 0
        avg_downdiff = 0
        prev_avg_updiff = 0
        prev_avg_downdiff = 0

        rsi = []
        rsi.append(None)

        for i in range(1, len(close_data)):
            diff = close_data[i] - close_data[i-1]

            if (i < span):
                if (diff  >= 0):
                    up_diffs.append(diff)
                else:
                    down_diffs.append(abs(diff))
                rsi.append(None)

            elif (i == span):
                avg_updiff = sum(up_diffs)/span
                avg_downdiff = sum(down_diffs)/span

                rsi.append(100 - ( 100 / (1 + (avg_updiff / avg_downdiff))))

                prev_avg_updiff = avg_updiff
                prev_avg_downdiff = avg_downdiff

            else:
                if (diff >= 0):
                    # Are these correct? Probably not
                    avg_updiff = ((span - 1) * prev_avg_updiff + diff) / span
                    avg_downdiff = ((span - 1) * prev_avg_downdiff) / span
                else:
                    avg_updiff = ((span - 1) * prev_avg_updiff) / span
                    avg_downdiff = ((span - 1) * prev_avg_downdiff + abs(diff)) / span
                    
                rsi.append(100 - ( 100 / (1 + (avg_updiff / avg_downdiff))))

                prev_avg_updiff = avg_updiff
                prev_avg_downdiff = avg_downdiff

        df['RSI'] = rsi

        plots.append(mpf.make_addplot(df['RSI'], panel=2))

        # Making horizontal lines for oversold/overbought signals
        oversold_sig = []
        overbought_sig = []

        for i in range(0, len(df.index)):
            oversold_sig.append(30)
            overbought_sig.append(70)

        # Plotting #########################################################
        plots.append(mpf.make_addplot(oversold_sig, panel=2, color='r', secondary_y=False))
        plots.append(mpf.make_addplot(overbought_sig, panel=2, color='r', secondary_y=False))
        ####################################################################

    except:
        print("RSI was not added due to an error. Check if DataFrame is correct.")
