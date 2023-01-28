# Use yahoo finance for extracting market information
from sqlite3 import Date

import row as row
import ta
import yfinance as yf
# import ta for calculating technical indicators
from ta import add_all_ta_features
#  Use panda for handling data
import pandas as pd
from pandas.core import window
# import numpy
import numpy as np
# Use matplotlib for visualising the trading strategy
import matplotlib.pyplot as plt
# use date time built-in library for manipulating date and time data
from datetime import datetime

from yfinance import data


# commit

def stochrsi_cal(asset):
    df = yf.download(asset, start="2021-01-01", rounding=True, interval='1d')
    df['sma_200'] = ta.trend.sma_indicator(df.Close, window=200)
    df['stoch_k'] = ta.momentum.stochrsi_k(df.Close, window=10)
    df.dropna(inplace=True)
    df.loc[(df['Close'] > df['sma_200']) & (df['stoch_k'] < 0.05), 'Buy'] = 'Yes'
    df.loc[(df['Close'] < df['sma_200']) | (df['stoch_k'] > 0.05), 'Buy'] = 'No'
    # df['buy'] = (df.Close > df.sma_200) & (df.stoch_k < 0.05)
    pd.set_option('display.max_row', None)
    df = pd.DataFrame(df)

    return df


print(stochrsi_cal('BTC-USD')[['Close', 'Low', 'sma_200', 'stoch_k', 'Buy']])


def get_signals(df):
    buying_dates = []
    selling_dates = []
    buying_prices = []
    selling_prices = []

    for i in range(len(df)):
        if "Yes" in df['Buy'].iloc[i]:
            buying_dates.append(df.iloc[i + 1].name)
            buying_prices.append(df.iloc[i + 1].Close)
            for j in range(1, 11):
                if df['Close'].iloc[i + j] > df.iloc[i + 1].Close * 1.03:
                    selling_dates.append(df.iloc[i + j + 1].name)
                    selling_prices.append(df.iloc[i + j + 1].Close)
                    break
                elif j == 10:
                    selling_dates.append(df.iloc[i + j + 1].name)
                    selling_prices.append(df.iloc[i + j + 1].Close)

            return buying_dates, buying_prices, selling_dates, selling_prices


data_frame = stochrsi_cal('BTC-USD')
buying_dates, selling_dates, buying_prices, selling_prices = data_frame

print(buying_prices)
