import datetime as dt
import pandas as pd
from abc import ABC, abstractmethod

class indicator(ABC):

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def signal_at(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_data(self):
        pass

class sma(indicator):
    def __init__(self, mdata, span=20, rowname='Close'):
        self.__type = "sma"
        self.__data = pd.DataFrame()
        self.__span = span
        self.__rowname = rowname
        
        self.__calc_data(mdata)


    def __calc_data(self, mdata):
        col_name = "SMA " + str(self.__span)
        self.__data[col_name] = mdata[self.__rowname].rolling(window=self.__span).mean()

        self.__data['Date'] = mdata['Date']
        self.__data.set_index('Date', inplace=True)

    def __calc_signal(self):
        pass
        # TODO

    def update(self, mdata):
        self.__data.drop(self.__data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

class ema(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self.__type = "ema"
        self.__data = pd.DataFrame()

        self.__span = span
        self.__rowname = rowname

        self.__calc_data(mdata)

    def __calc_data(self, mdata):
        col_name = "EMA " + str(self.__span)
        self.__data[col_name] = mdata[self.__rowname].ewm(span=self.__span, adjust=False).mean()

        self.__data['Date'] = mdata['Date']
        self.__data.set_index('Date', inplace=True)

    def __calc_signal(self):
        pass
        # TODO

    def update(self, mdata):
        self.__data.drop(self.__data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

class macd(indicator):
    count = 0
    def __init__(self, mdata, span1=12, span2=26, signalspan=9, rowname="Close"):
        self.__type = "ema"
        self.__data = pd.DataFrame()
        self.__span1 = span1
        self.__span2 = span2
        self.__signalspan = signalspan
        self.__last_signal = None

        macd.count += 1

        self.__name = "MACD " + str(macd.count)
        self.__signal_name = self.__name + " Signal"

        self.__calc_data(mdata, rowname)

    def __calc_data(self, mdata, rowname='Close'):
        ema1 = mdata[rowname].ewm(span=self.__span1, adjust=False).mean()
        ema2 = mdata[rowname].ewm(span=self.__span2, adjust=False).mean()

        macd_line = ema1 - ema2
        signal_line = macd_line.ewm(span=self.__signalspan, adjust=False).mean()

        self.__data[self.__name] = ema1 - ema2
        self.__data[self.__signal_name] = signal_line

        self.__calc_signal(macd_line, signal_line)

        self.__data['Date'] = mdata['Date']
        self.__data.set_index('Date', inplace=True)

       
    def __calc_signal(self, macd_line, signal_line):
        flag = False

        buy_sell = []

        if (macd_line[0] > signal_line[0]):
            flag = True

        for i in range(len(macd_line)):
            if (macd_line[i] > signal_line[i] and flag == False):
                buy_sell.append("buy")
                flag = True
            
            elif (macd_line[i] < signal_line[i] and flag == True):
                buy_sell.append("sell")
                flag = False

            else:
                buy_sell.append(None)

        self.__data['Buy/Sell'] = buy_sell

    def update(self, mdata):
        self.__data.drop(self.__data.index, inplace=True)
        self.__calc_data(mdata)

    def signal_at(self, datetime):
        return self.__data.loc[datetime, 'Buy/Sell']

    def get_type(self):
        return self.__type
    
    def get_data(self):
        return self.__data

class rsi(indicator):
    def __init__(self, mdata, span=14, rowname='Close', overbought_percent=70, oversold_percent=30):
        self.__type = "rsi"
        self.__data = pd.DataFrame()

        self.__span = span
        self.__overbought_percent = overbought_percent
        self.__oversold_percent = oversold_percent

        self.__name = "RSI"

        self.__calc_data(mdata)

    def __calc_data(self, mdata, rowname='Close'):
        close_data = mdata[rowname]

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

            if (i < self.__span):
                if (diff  >= 0):
                    up_diffs.append(diff)
                else:
                    down_diffs.append(abs(diff))
                rsi.append(None)

            elif (i == self.__span):
                avg_updiff = sum(up_diffs)/self.__span
                avg_downdiff = sum(down_diffs)/self.__span

                rsi.append(100 - ( 100 / (1 + (avg_updiff / avg_downdiff))))

                prev_avg_updiff = avg_updiff
                prev_avg_downdiff = avg_downdiff

            else:
                if (diff >= 0):
                    # Are these correct? Probably not
                    avg_updiff = ((self.__span - 1) * prev_avg_updiff + diff) / self.__span
                    avg_downdiff = ((self.__span - 1) * prev_avg_downdiff) / self.__span
                else:
                    avg_updiff = ((self.__span - 1) * prev_avg_updiff) / self.__span
                    avg_downdiff = ((self.__span - 1) * prev_avg_downdiff + abs(diff)) / self.__span
                    
                rsi.append(100 - ( 100 / (1 + (avg_updiff / avg_downdiff))))

                prev_avg_updiff = avg_updiff
                prev_avg_downdiff = avg_downdiff

        self.__data[self.__name] = rsi
        self.__calc_signal()

        self.__data['Date'] = mdata['Date']
        self.__data.set_index('Date', inplace=True)

    def __calc_signal(self): # Temporary implementation
        flag = False

        buy_sell = []
        data = self.__data[self.__name]

        for i in range(len(self.__data.index)):
            if (data[i] > self.__overbought_percent and flag == False):
                buy_sell.append("buy")
                flag = True
            
            elif (data[i] < self.__oversold_percent and flag == True):
                buy_sell.append("sell")
                flag = False

            else:
                buy_sell.append(None)

        self.__data['Buy/Sell'] = buy_sell

    def update(self, mdata):
        self.__data.drop(self.__data.index, inplace=True)
        self.__calc_data(mdata)

    def signal_at(self, datetime):
        return self.__data.loc[datetime, 'Buy/Sell']

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

class bollinger(indicator):
    def __init__(self, mdata, span=20, deviations=2):
        self.__type = "bollinger"
        self.__data = pd.DataFrame()
        self.__span = span
        self.__deviations = deviations

        self.__calc_data(mdata)
        

    def __calc_data(self, mdata):
        tp = mdata.iloc[:, [0, 1, 3]].mean(axis=1)
        self.__data['SMA BOLL'] = mdata['Close'].rolling(window=self.__span).mean()

        self.__data['BOLU'] = self.__data['SMA BOLL'] - self.__data['SMA BOLL'] - tp.rolling(window=self.__span).std() * self.__deviations
        self.__data['BOLD'] = self.__data['SMA BOLL'] - self.__data['SMA BOLL'] + tp.rolling(window=self.__span).std() * self.__deviations

        self.__calc_signal()

        self.__data['Date'] = mdata['Date']
        self.__data.set_index('Date', inplace=True)

    def __calc_signal(self):
        pass

    def update(self, mdata):
        self.__data.drop(self.__data.index, inplace=True)
        self.__calc_data(mdata)

    def signal_at(self, datetime):
        pass

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

