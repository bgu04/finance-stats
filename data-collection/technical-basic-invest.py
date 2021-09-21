import pymongo
from datetime import date
import sys


if len(sys.argv) == 1:
    today = date.today()
    dateStr = today.strftime("%d/%m/%Y")
else:
    dateStr = sys.argv[1]

print('Input date string:', dateStr)

def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = mongo_client["finance"]
    print('DB connected')
    return db[collName]


stock_info_coll = getDBCollection("stock_info")
stock_tech_coll = getDBCollection("stock_technicals")
stock_fundamentals_coll = getDBCollection("stock_fundamentals")
stock_port_coll = getDBCollection("stock_portfolios")

res_map = {}
for i in range(0, 13):
    res_map[i] = []

for s in stock_tech_coll.find({'date': dateStr}):

    count = 0
    for t in s.keys():
        if t == '_id' or t == 'symbol' or t == 'date':
            continue
        elem = s[t]
        #print(elem)
        if elem['signal'] == 'buy':
            count += 1
    # print(count)
    res_map[count].append(s)


for i in range(0, 13):
    print(i, len(res_map[i]))


portfolio = []
portfolio.extend(res_map[11])
portfolio.extend(res_map[10])

fund = {}
fund['name'] = 'Basic Invest'
fund['portId'] = 'BI-1'
fund['date'] = dateStr
fund['current_value'] = 1000000
portfolio_picked = []
for tt in portfolio:
    info = stock_fundamentals_coll.find_one({'symbol': tt['symbol']})
    if info['marketCap'] != '-' and int(info['marketCap']) > 3000000000 and info['eps'] != '-' and int(info['eps']) > 0 and info['oneYearReturn'] != '-' and float(info['oneYearReturn'].replace('%', '')) > 30:
        print(tt['symbol'], info['revenue'],  info['eps'],  info['volume'],
              info['marketCap'], info['ratio'], info['beta'], info['oneYearReturn'],
              info['sharesOutstanding'])
        picked = info.copy()
        portfolio_picked.append(picked)

for s in portfolio_picked:
    s['share'] = float(fund['current_value']) / len(portfolio_picked) / float(s['prevClose'])     
fund['portfolio'] = portfolio_picked 
stock_port_coll.insert_one(fund)