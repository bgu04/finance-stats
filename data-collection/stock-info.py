'''
Establish stock basic info collection in MongoDB by calling twelve-data APIs.
- Ben

Stock info example:
{
    'symbol': 'YVR', 
    'name': 'Liquid Media Group Ltd', 
    'currency': 'USD', 
    'exchange': 'NASDAQ', 
    'country': 'United States', 
    'type': 'Common Stock'
}

'''

import pymongo
import requests

def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["finance"]
    print('DB connected')
    return db[collName]


URL = "https://twelve-data1.p.rapidapi.com/stocks"
EXCHANGE = 'NASDAQ'
# EXCHANGE = 'NYSE'

headers = {
    'x-rapidapi-host': 'twelve-data1.p.rapidapi.com',
    'x-rapidapi-key': 'f6001cd7demsh8ba79a5c5fc120bp180fd8jsn35b15f301fc6'
}


response = requests.get(
    URL,
    params = {'exchange': EXCHANGE, 'format': 'json'},
    headers = headers
)

json_response = response.json()
stock_info_coll = getDBCollection("stock_info")

count = 0
for stock in json_response['data']:
    stock_info_coll.insert_one(stock)
    count += 1

print('inserted ', count, 'stocks')