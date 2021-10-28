'''

This program removes duplicated records in stock_info collection.

'''

import pymongo
import requests

def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://192.168.1.155:27017/")
    db = mongo_client["finance"]
    print('DB connected')
    return db[collName]


EXCHANGE = 'NASDAQ'

stock_info_coll = getDBCollection("stock_info")

count = 0
for stock in stock_info_coll.find({}):
    dups = list(stock_info_coll.find({'symbol': stock['symbol']}))
    if len(dups) > 1:
        id = dups[0]['_id']
        stock_info_coll.delete_one({'_id': id})
        print('Removed dup for', stock['symbol'], id)

print('Done')