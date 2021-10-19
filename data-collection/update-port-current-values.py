import pymongo
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
    return float(s['prevClose'])


for p in stock_port_coll.find({}):

    current_value = 0
    for s in p["portfolio"]:
        print (s['symbol'], s['share'])
        current_value += find_price(s['symbol'], dateStr) * float(s['share'])
    print (p['name'], current_value)
    print ('---------')
    return_rate = (current_value - float(p['origin_value'])) / float(p['origin_value'])
    stock_port_coll.update_one({'_id': p['_id']},  {'$set': {"current_value": current_value, "return_to_date": return_rate} } )