import investpy

df = investpy.get_stock_historical_data(stock='GOOG',
                                        country='United States',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')
print(df.head())

search_result = investpy.search_quotes(text='goog', products=['stocks'],
                                       countries=['united states'], n_results=1)
print(search_result)

recent_data = search_result.retrieve_recent_data()
print(recent_data.head())

historical_data = search_result.retrieve_historical_data(from_date='01/01/2019', to_date='01/01/2020')
print(historical_data.head())

information = search_result.retrieve_information()
print(information)

default_currency = search_result.retrieve_currency()
print(default_currency)


technical_indicators = search_result.retrieve_technical_indicators(interval="daily")
print(technical_indicators)