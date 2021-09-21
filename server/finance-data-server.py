from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
from flask_cors import CORS
from dateutil import parser
from bson.objectid import ObjectId
import time

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'finance'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/finance'

mongo = PyMongo(app)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/port/<string:id>', methods=['GET'])
def get_port_by_id(id):
    
    port_coll = mongo.db.stock_portfolios
    port = port_coll.find_one({'portId' : id})    
    port['_id'] = str(port['_id'])
    for p in port['portfolio']:
        p['_id'] = str(p['_id'])

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