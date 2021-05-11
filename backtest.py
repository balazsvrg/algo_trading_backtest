# Standard Library imports
from abc import ABC, abstractmethod
from tabulate import tabulate

# 3rd party imports
import pandas as pd

# local imports
import indicators as indicators

class Strategy(ABC):
    def __init__(self):
        self.indicators = []
        self._position_status = None

    @property
    def position_status(self):
        return self._position_status

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def next(self, index):
        pass
    
    def buy(self):
        self._position_status = 'buy'
    
    def sell(self):
        self._position_status = 'sell'

    def crossover(self, first, second, index):
        if index > 0:
            if first[index-1] < second[index-1] and first[index] > second[index]:
                return True
            else:
                return False
    

class Backtest:
    def __init__(self, cash, data, strategy):
        self._start_cash = cash
        self.cash = cash
        self.data = data
        self.strategy = strategy
        self.position = None
        self.trades = []

    def run(self):
        self.strategy.init()

        for i in range(len(self.data)):
            self.strategy.next(i)

            close_price = self.data.loc[i, 'Close']

            if self.strategy.position_status == 'buy' and self.position == None:
                self.position = Position(self.cash, close_price)
                self.cash -= self.position.entry_equity
                self.trades.append(Trade(close_price, i))
            
            if self.strategy.position_status == 'sell' and self.position is not None:
                self.cash += self.position.close(close_price)
                self.position = None
                self.trades[-1].close(close_price, i)
        
        if self.position is not None:
            self.cash += self.position.close(self.data.loc[len(self.data)-1, 'Close'])
            self.trades[-1].close(self.data.loc[len(self.data)-1, 'Close'], i)

        self.print_stats()
        # print("--Backtest Ran----------")
        # print(f"Starting cash: {self._start_cash}")
        # print(f"Ending cash: {self.cash}")
        # print(f"Profit: {self.cash / self._start_cash * 100}")

    def print_stats(self):
        exposure_time = 0
        for i in range(len(self.trades)):
            exposure_time += self.trades[i].exposure_time
        
        print(tabulate([["Exposure time (%)", exposure_time / len(self.data) * 100],
                        ["Starting cash: ", self._start_cash],
                        ["Ending cash: ", self.cash],
                        ["Profit (%): ", self.cash / self._start_cash * 100]],
                        headers=["Stat", "Value"], tablefmt='psql'))

    def plot(self):
        pass


class Trade:
    def __init__(self, entry_price, entry_time):
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.exposure_time = None
        self.exit_time = None
        self.exit_price = None
        self.profit = None

    def close(self, exit_price, exit_time):
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.exposure_time = self.exit_time - self.entry_time


class Position:
    def __init__(self, cash, entry_price):
        self.size = cash // entry_price
        self.entry_price = entry_price
        self._entry_equity = self.size * entry_price

    @property
    def entry_equity(self):
        return self._entry_equity

    def close(self, exit_price):
        return self.size * exit_price