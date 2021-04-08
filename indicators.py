import datetime as dt
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod

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

    def __calc_data(self, mdata):
        self._data['SMA'] = mdata[self._rowname].rolling(
            window=self._span).mean()

        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)

    def __calc_signal(self):
        pass
        # TODO

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

    def __calc_data(self, mdata):
        col_name = "EMA " + str(self._span)
        self._data[col_name] = mdata[self._rowname].ewm(
            span=self._span, adjust=False).mean()

        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)

    def __calc_signal(self):
        pass
        # TODO

    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)
        
    def signal_at(self, datetime):
        print("signal_at not yet implemented")
        # TODO


class macd(indicator):
    count = 0
    def __init__(
            self, mdata, span1=12, span2=26, signalspan=9, 
            rowname="Close"):
        self._type = "macd"
        self._data = pd.DataFrame()
        self._span1 = span1
        self._span2 = span2
        self._signalspan = signalspan
        self._last_signal = None

        macd.count += 1

        self._name = "MACD"
        self._signal_name = self._name + " Signal"

        self.__calc_data(mdata, rowname)

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data

    @property
    def span1(self):
        return self._span1

    # The function update() needs to be called after every parameter setting.  
    @span1.setter 
    def span(self, value):
        self._span1 = value
    
    @property
    def span2(self):
        return self._span2

    # The function update() needs to be called after every parameter setting.  
    @span2.setter
    def span2(self, value):
        self._span2 = value

    @property
    def signalspan(self):
        return self._signalspan

    # The function update() needs to be called after every parameter setting.  
    @signalspan.setter
    def signalspan(self, value):
        self._signalspan = value

    def __calc_data(self, mdata, rowname='Close'):
        ema1 = mdata[rowname].ewm(
            span=self._span1, adjust=False).mean()
        ema2 = mdata[rowname].ewm(
            span=self._span2, adjust=False).mean()

        macd_line = ema1 - ema2
        signal_line = macd_line.ewm(
            span=self._signalspan, adjust=False).mean()

        self._data[self._name] = ema1 - ema2
        self._data[self._signal_name] = signal_line

        self.__calc_signal(macd_line, signal_line)

        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)

       
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

        self._data['Buy/Sell'] = buy_sell

    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)

    def signal_at(self, datetime):
        return self._data.loc[datetime, 'Buy/Sell']


class rsi(indicator):
    def __init__(
            self, mdata, span=14, rowname='Close', 
            overbought_percent=70, oversold_percent=30):
        self._type = "rsi"
        self._data = pd.DataFrame()

        self._span = span
        self._overbought_percent = overbought_percent
        self._oversold_percent = oversold_percent

        self._name = "RSI"

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

    @property
    def overbought_percent(self):
        return self._overbought_percent
    
    # The function update() needs to be called after every parameter setting.  
    @overbought_percent.setter
    def overbought_percent(self, value):
        self._overbought_percent = value

    @property
    def oversold_percent(self):
        return self._oversold_percent

    # The function update() needs to be called after every parameter setting.  
    @oversold_percent.setter
    def oversold_percent(self, value):
        self._oversold_percent = value

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

            if (i < self._span):
                if (diff  >= 0):
                    up_diffs.append(diff)
                else:
                    down_diffs.append(abs(diff))
                rsi.append(None)

            elif (i == self._span):
                avg_updiff = sum(up_diffs) / self._span
                avg_downdiff = sum(down_diffs) / self._span

                rsi.append(100 - ( 100 / (1 + (avg_updiff / avg_downdiff))))

                prev_avg_updiff = avg_updiff
                prev_avg_downdiff = avg_downdiff

            else:
                if (diff >= 0):
                    avg_updiff = ((self._span - 1) 
                                 * prev_avg_updiff 
                                 + diff) / self._span
                    avg_downdiff = ((self._span - 1) 
                                 * prev_avg_downdiff) / self._span
                else:
                    avg_updiff = ((self._span - 1) 
                                 * prev_avg_updiff) / self._span
                    avg_downdiff = ((self._span - 1) 
                                 * prev_avg_downdiff 
                                 + abs(diff)) / self._span
                    
                rsi.append(100 - ( 100 / (1 + (avg_updiff / avg_downdiff))))

                prev_avg_updiff = avg_updiff
                prev_avg_downdiff = avg_downdiff

        self._data[self._name] = rsi
        self.__calc_signal()

        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)

    def __calc_signal(self):    # Temporary implementation  
        flag = False
        buy_sell = []
        data = self._data[self._name]

        for i in range(len(self._data.index)):
            if (data[i] > self._overbought_percent and flag == False):
                buy_sell.append("buy")
                flag = True
            
            elif (data[i] < self._oversold_percent and flag == True):
                buy_sell.append("sell")
                flag = False

            else:
                buy_sell.append(None)

        self._data['Buy/Sell'] = buy_sell

    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)

    def signal_at(self, datetime):
        return self._data.loc[datetime, 'Buy/Sell']


class bollinger(indicator):
    def __init__(self, mdata, span=20, deviations=2):
        self._type = "bollinger"
        self._data = pd.DataFrame()
        self._span = span
        self._deviations = deviations

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

    @property
    def deviations(self):
        return self._deviations

    # The function update() needs to be called after every parameter setting.  
    @deviations.setter
    def deviations(self, value):
        self._deviations = value

    def __calc_data(self, mdata):
        tp = mdata.iloc[:, [0, 1, 3]].mean(axis=1)
        self._data['SMA BOLL'] = mdata['Close'].rolling(
            window=self._span).mean()

        self._data['BOLU'] = ((self._data['SMA BOLL'] 
                             - self._data['SMA BOLL'])
                             - tp.rolling(window=self._span).std() 
                             * self._deviations)
        self._data['BOLD'] = ((self._data['SMA BOLL'] 
                             - self._data['SMA BOLL'])
                             + tp.rolling(window=self._span).std()
                             * self._deviations)

        self.__calc_signal()

        self._data['Date'] = mdata['Date']
        self._data.set_index('Date', inplace=True)

    def __calc_signal(self):
        pass

    def update(self, mdata):
        self._data.drop(self._data.index, inplace=True)
        self.__calc_data(mdata)

    def signal_at(self, datetime):
        pass


#a span igazából period
class mfi(indicator):
    def __init__(
            self, mdata, span=14, 
            overbought_percent=80, oversold_percent=20):
        self._type = "mfi"
        self._data = pd.DataFrame()

        self._span = span
        self._overbought_percent = overbought_percent
        self._oversold_percent = oversold_percent

        self._name = "MFI"

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

    @property
    def overbought_percent(self):
        return self._overbought_percent
    
    # The function update() needs to be called after every parameter setting.  
    @overbought_percent.setter
    def overbought_percent(self, value):
        self._overbought_percent = value

    @property
    def oversold_percent(self):
        return self._oversold_percent

    # The function update() needs to be called after every parameter setting.  
    @oversold_percent.setter
    def oversold_percent(self, value):
        self._oversold_percent = value

    def __calc_data(self, mdata):
        high_nums = mdata['High']
        low_nums = mdata['Low']
        close_nums = mdata['Close'] 
        typical_price = []
        money_flow = []
        positive_money_flow = []
        negative_money_flow = []
        positive_mf = []
        negative_mf = []


        typical_price = (high_nums + low_nums + close_nums) / 3
        money_flow = typical_price * mdata['Volume'] 

        for i in range(0, len(typical_price)):
            if typical_price[i] > typical_price[i-1]:
                positive_money_flow.append(money_flow[i-1])
                negative_money_flow.append(0)  
            elif typical_price[i] < typical_price[i-1]:
                 negative_money_flow.append(money_flow[i-1]) 
                 positive_money_flow.append(0) 
            else:
                positive_money_flow.append(0)
                negative_money_flow.append(0) 

        for i in range(self._span - 1, len(positive_money_flow)):
            positive_mf.append(sum(positive_money_flow[i + 1 - self._span : i+1]))
    
    
        for i in range(self._span - 1, len(negative_money_flow)):
            negative_mf.append(sum(negative_money_flow[i + 1 - self._span : i+1]))

        mfi = 100 * (np.array(positive_mf)/(np.array(positive_mf) + np.array(negative_mf)))

class obv(indicator):

    def __init__(
        self, mdata, span = 10 ):
        self.type = 'obv'
        self._data = pd.DataFrame()

        self._span = span
        self._name = "OBV"

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



    def __calc_data(mdata):
        obv = []
        obv.append(0)
        close = mdata['Close']
        volume = mdata['Volume']

        for i in range(1, len(close)):
            if close[i] > close[i-1]:
                obv.append(obv[-1] + volume[i])
            elif close[i] < close[i-1]:
                obv.append(obv[-1] - volume[i])
            else:
                obv.append(obv[-1])

class dema(indicator):

    def __init__(
        self, mdata, span = 10, rowname= 'close'):
        self.type = 'dema'
        self._data = pd.DataFrame()
        self._rowname = rowname

        self._span = span
        self._name = "DEMA"

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
    
    def __calc_data(mdata, span, rowname):

            ema = mdata[rowname].ewm(span=span, adjust = False).mean()
            dema = 2 * ema - ema.ewm(span=span, adjust = False).mean()
    
    return dema

    def __cals_signal(self):
            buy_list = [] 
            sell_list = []
            flag = False
    
    #dema shortot meg kell még csinálni meg a dema longot is 
        for i in range(0, len(data)):
            if self._data['DemaShort'][i] > self._data['DemaLong'][i] and flag = False:
                buy_list.append(self._data['Close'])
                sell_list.append(np.nan)
                flag = True
            elif self._data['DemaShort'][i] < self._data['DemaLong'][i] and flag = False:
                sell_list.append(self._data['Close'])
                buy_list.append(np.nan)
                flag = False
            else:
                buy_list.append(np.nan)
                sell_list.append(np.nan)

