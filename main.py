# Standard Library imports
import datetime as dt
import talib

# Relevant 3rd party imports
import mplfinance as mpf
import pandas as pd
import plotter as plt
import gspread

# Local imports
import indicators as ind
import backtest as bt

class MyStrategy(bt.Strategy):
    def init(self):
        self.indicators.append(ind.sma(OTP_DATA, span=10))
        self.indicators.append(ind.sma(OTP_DATA, span=20))
    
    def next(self, index):
        if self.crossover(self.indicators[0]['SMA'], self.indicators[1]['SMA'], index):
            self.buy()
        
        elif self.crossover(self.indicators[1]['SMA'], self.indicators[0]['SMA'], index):
            self.sell()



def main():
    smacross = MyStrategy()

    btest = bt.Backtest(500000.0, OTP_DATA, smacross)
    btest.run()

    indicators = [
                  ind.sma(OTP_DATA, span=10),
                  ind.sma(OTP_DATA, span=20),
                  ]

    plotter = plt.plotter(OTP_DATA)


    for i in indicators:
        plotter.add_plot(i)

    plotter.plot()


if __name__ == "__main__":
    OTP_DATA =  pd.read_csv('data.csv')
    main()
