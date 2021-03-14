import pandas as pd
import mplfinance as mpf

class plotter:
    def __init__(self, market_data, title="Stock Data"):
        self.market_data = market_data
        self.plots = pd.DataFrame()
        self.titlestring = title

    def plot(self, type = 'candle', style = 'yahoo', volume = True):
        mpf.plot(self.market_data, type=type, style=style, title=self.titlestring, volume=volume, addplot=self.plots)

    def add_plot(self, plot_data, indicator_type):
        if (indicator_type == 'sma' or indicator_type == 'SMA'):
            self.plots.append(mpf.make_addplot(plot_data['SMA'], panel = 0))