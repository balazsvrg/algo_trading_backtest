import pandas as pd
import mplfinance as mpf
import indicators as ind

class plotter:
    def __init__(self, mdata=None, type="candle", title="Stock Data", style="yahoo", plot_volume=True):
        self.mdata = mdata
        self.type = type
        self.title = title
        self.style = style
        self.plot_volume = plot_volume
        self._indicators = []
        self._hlines = []

        self.mdata['Date'] = pd.to_datetime(self.mdata['Date'])
        self.mdata.set_index('Date', inplace=True)

    def plot(self):
        mpf.plot(self.mdata, hlines=self._hlines, type=self.type, style=self.style, title=self.title, volume=self.plot_volume, addplot=self._indicators)


    def add_plot(self, indicator):
        if (indicator.type == "sma"):
            self._indicators.append(mpf.make_addplot(indicator.data, panel = 0))

        elif (indicator.type == "ema"):
            self._indicators.append(mpf.make_addplot(indicator.data, panel = 0))

        elif (indicator.type == "macd"):
            self._indicators.append(mpf.make_addplot(indicator.data["MACD"], panel = 1, color='g', secondary_y=True))
            self._indicators.append(mpf.make_addplot(indicator.data["MACD Signal"], panel = 1, color='b', secondary_y=True))

        elif (indicator.type == "rsi"):
            self._indicators.append(mpf.make_addplot(indicator.data["RSI"], panel = 2, color='b', secondary_y=True))
            self._hlines.append(indicator.overbought_percent)
            self._hlines.append(indicator.oversold_percent)

        elif (indicator.type == "bollinger"):
            self._indicators.append(mpf.make_addplot(indicator.data, panel = 0))
