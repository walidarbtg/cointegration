import requests


fapi_url = "https://fapi.binance.com"

# Response format: open time, open, high, low, close, volume, close time, etc...
def get_historical_prices(symbol, interval, startTime, endTime):
    route = "/fapi/v1/klines"
    try:
        resp = requests.get(fapi_url + route, params={'symbol': symbol, 'interval': interval, 'startTime': startTime, 'endTime': endTime, 'limit': 1000})
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(e) 


def get_all_tickers():
    route = '/fapi/v1/ticker/24hr'
    try:
        resp = requests.get(fapi_url + route)
        return resp.json()
    except requests.exceptions.RequestException as e:
        print(e)