import binance_api
import math
import pandas as pd
from datetime import datetime


def get_historical_data(symbol, interval, startTime, endTime):
    batch_limit = 1000
    startDate = datetime.fromtimestamp(round(startTime/1000))
    endDate = datetime.fromtimestamp(round(endTime/1000))
    delta = endDate - startDate

    # calculate how many data points we need to fetch to know how many batch call needed
    if interval == '1m':
        data_points = delta.days * 24 * 60
        nbr_of_batch = math.ceil(data_points / batch_limit)
    elif interval == '1h':
        data_points = delta.days * 24
        nbr_of_batch = math.ceil(data_points / batch_limit)
    elif interval == '4h':
        data_points = delta.days * 24 / 4
        nbr_of_batch = math.ceil(data_points / batch_limit)
    elif interval == '1d':
        data_points = delta.days
        nbr_of_batch = math.ceil(data_points / batch_limit)
    else:
        print("Incorrect interval")
        return

    print('Download data in {} chunks'.format(nbr_of_batch))
    historical_data = pd.DataFrame()
    for i in range(0, nbr_of_batch):
        if i != 0:
            startTime = endTime

        if interval == '1m':
            # 60 seconds times 1000 minutes * 1000 to get milliseconds
            endTime = startTime + batch_limit * 60 * 1000
        elif interval == '1h':
            endTime = startTime + batch_limit * 60 * 60 * 1000
        elif interval == '4h':
            endTime = startTime + batch_limit * 4 * 60 * 60 * 1000
        elif interval == '1d':
            endTime = startTime + batch_limit * 24 * 60 * 60 * 1000
        
        chunk = binance_api.get_historical_prices(symbol, interval, startTime, endTime)
        historical_data = pd.concat([historical_data, pd.DataFrame(chunk)])
        print('{} of {}'.format(i+1, nbr_of_batch))

    return historical_data

startTime = round(datetime(2020, 1, 1).timestamp()) * 1000
endTime = round(datetime(2022, 1, 1).timestamp()) * 1000
historical_data = get_historical_data('BTCUSDT', '1h', startTime, endTime)

historical_data.to_csv('./BTCUSDT_1h_2020_to_2022.csv')
print('Done')