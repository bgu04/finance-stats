from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS
from dateutil import parser
from bson.objectid import ObjectId
import time
from datetime import datetime
from datetime import date
import requests


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'finance'
app.config['MONGO_URI'] = 'mongodb://192.168.1.155:27017/finance'

mongo = PyMongo(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

last_update_on_benchmark = datetime.now()

def get_spy_benchmark():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPY&apikey=Y0Y9D9IXUGG5PJ11'
    r = requests.get(url)
    data = r.json()
    last_update_on_benchmark = datetime.now()
    print("Benchmark updated and timestamp set to:", last_update_on_benchmark)
    return data['Time Series (Daily)']

def update_benchmark():
    now = datetime.now()
    if (now - last_update_on_benchmark).days > 0:
        get_spy_benchmark()

benchmarks = get_spy_benchmark()

def normalize(array):
    base = float(array[0]['y'])
    for a in array:
        a['y'] = int( float(a['y'])/ base * 100 )

@app.route('/api/port/<string:id>', methods=['GET'])
def get_port_by_id(id):
    
    update_benchmark()
    print(benchmarks)

    port_coll = mongo.db.stock_portfolios
    port = port_coll.find_one({'portId' : id})    
    port['_id'] = str(port['_id'])
    for p in port['portfolio']:
        p['_id'] = str(p['_id'])

    # adding benchmark data
    series = port['performance']
    bm = []
    for d in series:
        print(d)
        time_string = datetime.fromtimestamp(int(d['x']/1000) - 86400).strftime('%Y-%m-%d')
        bm.append({
                'x': d['x'],
                'y': benchmarks[time_string]["5. adjusted close"]
            })

    normalize(bm)
    normalize(port['performance'])
    port['benchmark'] = bm

    response = jsonify(port)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


@app.route('/api/ports', methods=['GET'])
def get_ports():
    
    port_coll = mongo.db.stock_portfolios
    res = []
    for port in port_coll.find({}):
        port['_id'] = str(port['_id'])
        for p in port['portfolio']:
            p['_id'] = str(p['_id'])
        res.append(port)

    response = jsonify(res)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

if __name__ == '__main__':
    app.run(app.run(host="localhost", port=5001, debug=True))