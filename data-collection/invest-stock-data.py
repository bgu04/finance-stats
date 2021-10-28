import pymongo
import investpy
from datetime import date

today = date.today()
dateStr = today.strftime("%d/%m/%Y") 

def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://192.168.1.155:27017/")
    db = mongo_client["finance"]
    print('DB connected')
    return db[collName]


stock_info_coll = getDBCollection("stock_info")
stock_tech_coll = getDBCollection("stock_technicals")
stock_fundamentals_coll = getDBCollection("stock_fundamentals")

count = 0
for stock in stock_info_coll.find():
    print(stock)

    sym = stock['symbol']

    existing = stock_tech_coll.find({'$and': [{'date': dateStr }, {'symbol': sym }]})
    print(existing)
    
    if len(list(existing)) > 0:
        print('skip it:', stock['symbol'])
        continue
    else:
        print('doing it:', stock['symbol'])

    try:
        search_result = investpy.search_quotes(text= stock['symbol'], products=['stocks'],
                                        countries=['united states'], n_results=1)

        count += 1
        
        information = search_result.retrieve_information()
        # print(information)
        information['date'] = dateStr
        information['symbol'] = stock['symbol']
        stock_fundamentals_coll.insert_one(information)

        technical_indicators = search_result.retrieve_technical_indicators(interval="daily")
        
        techs = {}
        techs['symbol'] = stock['symbol']
        techs['date'] = dateStr
        for t in technical_indicators.values.tolist():
            elem = {}
            elem['signal'] = t[1]
            elem['value'] = t[2]
            techs[ t[0] ] = elem
        # print(techs) #.to_json(orient='index')
        stock_tech_coll.insert_one(techs)

    except:
        print("Error getting: ", stock['symbol'])

    