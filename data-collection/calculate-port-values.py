#
#  The program will:
#  1. retrieve the stock prices of each portofolio. 
#  2. calculate the portofolio values of all days since start and save them into DB. 
#  3. calculate overall portofolio values and performance number. 
#


import pymongo
from datetime import datetime
from datetime import date
import sys
from utilities import getDBCollection


if len(sys.argv) == 1:
    today = date.today()
    dateStr = today.strftime("%d/%m/%Y")
else:
    dateStr = sys.argv[1]

print('Input date string:', dateStr)


stock_info_coll = getDBCollection("stock_info")
stock_tech_coll = getDBCollection("stock_technicals")
stock_fundamentals_coll = getDBCollection("stock_fundamentals")
stock_port_coll = getDBCollection("stock_portfolios")


def find_price(symbol, day_string):
    s = stock_fundamentals_coll.find_one({'$and': [{'symbol': symbol}, {'date': day_string}]})
    if s == None:
        return -1.0
    else:
        return float(s['prevClose'])


def  find_prices(symbol):

    f_series = stock_fundamentals_coll.find({'symbol': symbol})

    sortedList = []
    for s in f_series:
        sortedList.append(s)

    sorted(sortedList, 
        key=lambda k: datetime.strptime(k['date'], "%d/%m/%Y") )

    return sortedList


for port in stock_port_coll.find({}):

    port_value_map = {}

    current_value = 0
    for s in port["portfolio"]:
        # print (s['symbol'], s['share'])
        orig_date = datetime.strptime(port['date'], "%d/%m/%Y")
        price_list = find_prices(s['symbol'])
        for p in price_list:
            if datetime.strptime(p['date'], "%d/%m/%Y") < orig_date:
                continue

            if p['date'] in port_value_map:
                port_value_map[p['date']] += float(p['prevClose']) * float(s['share'])
            else:
                port_value_map[p['date']] = float(p['prevClose']) * float(s['share'])


    keys = list(port_value_map.keys())

    values = []
    for k in keys:
        values.append( {
            'x': int(datetime.strptime(k, "%d/%m/%Y").timestamp() * 1000),
            'y': int(port_value_map[k] / 10000)
        })

    print(values)

    stock_port_coll.update_one({'_id': port['_id']},  {'$set': {"performance": values } })