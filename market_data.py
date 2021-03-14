import numpy as np
import pandas as pd
import mplfinance as mpf

class market_data:
    def __init__(self, df):
        self.ohlc = df
        self.indicators = pd.DataFrame()
        self.has_sma = False
        self.has_ema = False
        self.has_macd = False
        self.has_rsi = False
        self.has_bollinger = False

    def add_sma(self, span=20, name='SMA', row='Close') -> pd.DataFrame:
        try:
            self.indicators[name] = self.ohlc[row].rolling(window=span).mean()

            self.has_sma = True
        except:
            print("SMA {} was not added due to an error. Check if DataFrame is correct.", span)

    def add_ema(self, span=20, name='EMA', row='Close'):
        try:
            self.indicators[name] = self.ohlc[row].ewm(span=span, adjust=False).mean()

            self.has_ema = True

            # Plotting ########################################
            # plots.append(mpf.make_addplot(df['EMA {}', span]))
            # ###################################################
        except:
            print("EMA {} was not added due to an error. Check if DataFrame is correct.", span)

    def add_macd(self, name='MACD', row='Close', span1=12, span2=26, signalspan=9):
        try:
            ema1 = self.ohlc[row].ewm(span=span1, adjust=False).mean()
            ema2 = self.ohlc[row].ewm(span=span2, adjust=False).mean()
            self.indicators[name] =  ema1 - ema2
            signal_name = name + " signal"
            self.indicators[signal_name] = self.indicators['MACD'].ewm(span=signalspan, adjust=False).mean()

            self.has_macd = True

            # Plotting ########################################
            # plots.append(mpf.make_addplot(df['MACD'], panel=1, secondary_y=True))
            # plots.append(mpf.make_addplot(df['MACD SIGNAL'], panel=1, secondary_y=True))
            ###################################################

        except:
            print("MACD was not added due to an error. Check if DataFrame is correct.")

    def add_rsi(self, name='RSI', span = 14, overbought_percent=70, oversold_percent=30):
        try:
            close_data = []

            for row in self.ohlc.itertuples():
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

            self.indicators[name] = rsi

            # plots.append(mpf.make_addplot(df['RSI'], panel=2))

            # Making horizontal lines for oversold/overbought signals
            oversold_sig = []
            overbought_sig = []

            for i in range(0, len(self.ohlc.index)):
                oversold_sig.append(oversold_percent)
                overbought_sig.append(overbought_percent)

            os_name = name + " oversold"
            ob_name = name + " overbought"
            self.indicators[os_name] = oversold_sig
            self.indicators[ob_name] = overbought_sig

            self.has_rsi = True

            # Plotting #########################################################
            # plots.append(mpf.make_addplot(oversold_sig, panel=2, color='r', secondary_y=False, width=1, linestyle='dashdot'))
            # plots.append(mpf.make_addplot(overbought_sig, panel=2, color='r', secondary_y=False, width=1, linestyle='dashdot'))
            ####################################################################

        except:
            print("RSI was not added due to an error. Check if DataFrame is correct.")

    def add_bollinger(self, span = 20, deviations = 2):
        tp = self.ohlc.iloc[:, [0, 1, 3]].mean(axis=1)
        self.add_sma(name='SMA BOLL', span=span)

        self.indicators['BOLU'] = self.indicators['SMA BOLL'] - tp.rolling(window=span).std() * deviations
        self.indicators['BOLD'] = self.indicators['SMA BOLL'] + tp.rolling(window=span).std() * deviations

        self.has_bollinger = True

        # Plotting ########################################################
        # plots.append(mpf.make_addplot(df['SMA BOLL'], panel=0))
        # plots.append(mpf.make_addplot(df['BOLU'], panel=0, color='gray'))
        # plots.append(mpf.make_addplot(df['BOLD'], panel=0, color='gray'))
        ###################################################################

