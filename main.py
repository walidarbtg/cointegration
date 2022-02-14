import binance_api
import numpy as np
import pandas as pd

import statsmodels
from statsmodels.tsa.stattools import coint
import statsmodels.api as stat
import statsmodels.tsa.stattools as ts

import matplotlib.pyplot as plt
from datetime import datetime, date

# https://www.marketcalls.in/amibroker/computing-cointegration-and-augmented-dickey-fuller-test-in-amibroker-using-python.html#:~:text=Augmented%20Dicky%20Fuller%20test%20is,stationary%20and%20cointegrated%20or%20not.&text=The%20Augmented%20Dicky%20Fuller%20test,want%20to%20reject%20this%20hypothesis.

# default values
nbr_of_coins = 20
interval = '1d'
lookback_period = 7
startTime = round(datetime(2020, 1, 1).timestamp()) * 1000
endTime = round(datetime(2022, 1, 1).timestamp()) * 1000

# Get all coins, sort them by volume and keep the top x nbr of coins
tickers = pd.DataFrame(binance_api.get_all_tickers())
tickers['volume_usd'] = tickers.apply(lambda row: float(row['volume']) * float(row['lastPrice']), axis=1)
tickers = tickers.sort_values(by='volume_usd', ascending=False)
top_tickers = tickers[:nbr_of_coins]
print(top_tickers['symbol'])

# Get historical data
historical_data = {}
for i in range(0, len(top_tickers)):
    historical_data[top_tickers.iloc[i]['symbol']] = pd.DataFrame(binance_api.get_historical_prices(top_tickers.iloc[i]['symbol'], interval, startTime, endTime))

# Do cointegration
data_1 = np.asarray(historical_data['BTCUSDT'][4].tail(lookback_period)).astype(float)
data_2 = np.asarray(historical_data['ETHUSDT'][4].tail(lookback_period)).astype(float)
result = stat.OLS(data_1, data_2).fit()
a = ts.adfuller(result.resid)
print('p-value: {}'.format(a[1]))
