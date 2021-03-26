import datetime as dt
import pandas as pd
from abc import ABC, abstractmethod

class indicator(ABC):

    @apstractmethod
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

        self.__calc_data(mdata, span, rowname)


    def __calc_data(self, mdata, span, rowname):
        col_name = "SMA " + span
        self.__data[col_name] = mdata[rowname].rolling(window=span).mean()

    def __calc_signal(self):
        pass
        # TODO

    def update(self, mdata):
        self.__calc_data(mdata)
        
    def signal_at():
        pass
        # TODO

    def get_type(self):
        return self.__type

    def get_data(self):
        return self.__data

class ema(indicator):
    def __init__(self):
        self.__type = "ema"
        self.__data = pd.DataFrame()

    def calc_data(self, mdata, span=20, rowname='Close'):
        col_name = "EMA " + span
        self.__data[col_name] = mdata[rowname].ewm(span=span, adjust=False).mean()

    def __calc_signal(self):
        pass
        # TODO

    def update(self, mdata):
        self.__calc_data(mdata)
        
    def signal_at():
        pass
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

        self.__data['Date'] = mdata['Date']

        self.__data[self.__name] = ema1 - ema2
        self.__data[self.__signal_name] = signal_line

        self.__calc_signal(macd_line, signal_line)

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