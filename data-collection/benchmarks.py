'''
From Alpha Vantage APIs: https://www.alphavantage.co/documentation/
key = Y0Y9D9IXUGG5PJ11
'''

import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPY&apikey=Y0Y9D9IXUGG5PJ11'
r = requests.get(url)
data = r.json()


time_series = data['Time Series (Daily)']
print(time_series)
