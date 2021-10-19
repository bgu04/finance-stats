
import pymongo

def getDBCollection(collName):
    mongo_client = pymongo.MongoClient("mongodb://192.168.1.155:27017/")
    db = mongo_client["finance"]
    print('DB connected')
    return db[collName]