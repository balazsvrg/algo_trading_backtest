# Standard Library imports
import datetime as dt
from abc import ABC, abstractmethod
import talib as ta
import numpy as np

# 3rd party imports
import pandas as pd

class indicator(ABC):
    """Base class for all indicators

    Properties:
        type (str): Type of indicator represented in short.
        data (pandas.DataFrame): Calculated values of the indicator.
    """
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def signal_at(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass


class sma(indicator):
    """Simple moving average indicator.

    Calculates the non-weighted average of the closing prices on a 
    given dataset.

    Properties:
        type: Type of the indicator (set to 'sma' by default)
        data: Calculated sma on the given dataset.
        span: Number of datapoints used in the calculation
    """
    def __init__(self, mdata, span=20, rowname='Close'):
        self._type = "sma"
        self._data = pd.DataFrame()
        self._span = span
        self._rowname = rowname
        
        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value
    
    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):

        close = mdata['Close']
        sma = ta.SMA(close, timeperiod=self._span)
        self._data['SMA'] = sma
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)

    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO


class ema(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "ema"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        time = self._span
        ema = ta.EMA(close, timeperiod=time)


        col_name = "EMA " + str(self._span)
        
        self._data[col_name] = ema
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class cci(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "cci"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        time = self._span
        cci = ta.CCI(high, low, close, timeperiod=time)


        col_name = "CCI " + str(self._span)
        
        self._data[col_name] = cci
 
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class macd(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "macd"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        macd = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)


        col_name = "MACD " + str(self._span)
        
        self._data[col_name] = macd
 
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class mfi(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "mfi"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        mfi = ta.MFI(high, low, close, volume)


        col_name = "MFI " + str(self._span)
        
        self._data[col_name] = mfi
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class tema(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "tema"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        tema = ta.TEMA(close, timeperiod=30)


        col_name = "TEMA " + str(self._span)
        
        self._data[col_name] = tema
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO


class dema(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "dema"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        dema = ta.DEMA(close, timeperiod=30)


        col_name = "DEMA " + str(self._span)
        
        self._data[col_name] = dema
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class rsi(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "rsi"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        rsi = ta.RSI(close, timeperiod=14)


        col_name = "RSI " + str(self._span)
        
        self._data[col_name] = rsi
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class wma(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "wma"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        wma = ta.WMA(close, timeperiod=30)


        col_name = "WMA " + str(self._span)
        
        self._data[col_name] = wma
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class bollinger(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "bollinger"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        floatclose = np.array(close)
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        bollinger = ta.BBANDS(floatclose, timeperiod=5, nbdevup=2, nbdevdn=2)


        col_name = "BOLLINGER " + str(self._span)
        
        self._data[col_name] = bollinger
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class roc(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "roc"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        roc = ta.ROC(close, timeperiod=10)
        

        col_name = "ROC " + str(self._span)
        
        self._data[col_name] = roc
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class stochrsi(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "stochrsi"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        stochrsi = ta.STOCHRSI(close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        

        col_name = "STOCHRSI " + str(self._span)
        
        self._data[col_name] = stochrsi
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class obv(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "obv"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        obv = ta.OBV(close, volume)
        

        col_name = "OBV " + str(self._span)
        
        self._data[col_name] = obv
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO

class sar(indicator):
    def __init__(self, mdata, span=20, rowname="Close"):
        self._type = "sar"
        self._data = pd.DataFrame()

        self._span = span
        self._rowname = rowname

        self.__calc_data(mdata)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span(self):
        return self._span

    # The function update() needs to be called after every parameter setting.  
    @span.setter 
    def span(self, value):
        self._span = value

    def __getitem__(self, index):
        return self._data[index]

    def __calc_data(self, mdata):


        close = mdata['Close']
        high = mdata['High']
        low = mdata['Low']
        volume = mdata['Volume']
        time = self._span
        sar = ta.SAR(high, low, acceleration=0.02, maximum=0.2)
        

        col_name = "SAR " + str(self._span)
        
        self._data[col_name] = sar
        """
        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)
        """
    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO
