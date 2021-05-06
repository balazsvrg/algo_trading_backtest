import datetime as dt
import mplfinance as mpf
import pandas as pd
import plotter as plt
import indicators as ind

def main():
    otp_data = pd.read_csv('data.csv')

    indicators = [
                  ind.sar(otp_data),
                  ]

    plotter = plt.plotter(otp_data)


    for i in indicators:
        plotter.add_plot(i)

    plotter.plot()


if __name__ == "__main__":
    main()
