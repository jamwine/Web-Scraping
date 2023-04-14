# This is just a placeholder for now, further feature analysis will be made once the bug is fixed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
from matplotlib.font_manager import FontProperties


class FeaturePlotting:
    def __init__(self):
        df = pd.read_csv('crypto_report2.csv')
        self.Stock = df["Stock"]
        self.Price = df["Price"].str.replace(',', '').astype(float).round(decimals=2)
        self.Market = df["Market"].str.replace('B', '')
        self.Supply = df["Supply"]
        self.Volume = df["Volume"]
        self.Change = df["Change"]
        self.Percent = df["Percent"]

        # Get Market Values of selected Stocks
        selector = df.loc[df['Stock'] == 'Bitcoin USD']
        self.Bitcoin = selector['Market'].str.replace('B', '').iloc[0]

        selector = df.loc[df['Stock'] == 'Ethereum USD']
        self.Ethereum = selector['Market'].str.replace('B', '').iloc[0]

        selector = df.loc[df['Stock'] == 'Tether USD']
        self.Tether = selector['Market'].str.replace('B', '').iloc[0]

        selector = df.loc[df['Stock'] == 'BNB USD']
        self.BNB = selector['Market'].str.replace('B', '').iloc[0]

        selector = df.loc[df['Stock'] == 'USD Coin USD']
        self.USD = selector['Market'].str.replace('B', '').iloc[0]

    def graph_settings(self):
        # Customizable Set-ups
        plt.figure(figsize=(12, 16))
        font = FontProperties()
        font.set_family('serif bold')
        font.set_style('oblique')
        font.set_weight('bold')
        ax = plt.axes()
        ax.set_facecolor("#e6eef1")

    def line_grpah(self):
        # Axis Initialization
        x = self.Price
        y = self.Change
        self.graph_settings()

        sb.lineplot(x=x, y=y, color='#01636e')
        plt.title("Price Fluctuations")
        plt.xlabel('Price Values', fontsize=15)
        plt.ylabel('Δ Price', fontsize=15)
        plt.grid(axis='y')
        plt.show()

    def bar_plot(self):
        # Axis Initialization
        x = (["Bitcoin USD", "Ethereum USD", "Tether USD", "BNB USD", "USD Coin USD"])
        y = ([float(self.Bitcoin), float(self.Ethereum), float(self.Tether), float(self.Bitcoin), float(self.USD)])
        self.graph_settings()

        plt.barh(x, y, color='#01636e')
        plt.title('Market Value for Top 5 Stocks')
        plt.show()


if __name__ == "__main__":
    data = FeaturePlotting()
    data.line_grpah()
    data.bar_plot()

