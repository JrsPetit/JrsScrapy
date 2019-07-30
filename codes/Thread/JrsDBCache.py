# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient
from pprint import pprint
from bson.son import SON
from datetime import datetime,timedelta
import time
try:
    import cPickle as pickle
except ImportError:
    import pickle
import zlib
from bson.binary import Binary

class MongoCache:
    def __init__(self, client=None, expires = timedelta(days=30)):
        self.client = MongoClient('localhost',27017) if client is None else client
        self.db = self.client.cachePro
        self.db.webpage.create_index('timestamp',expireAfterSeconds = expires.total_seconds())

    def __getitem__(self,url):
        record = self.db.webpage.find_one({'_id':url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + 'does not exist')
    
    def __setitem__(self,url,result):
        record = {'result':Binary(zlib.compress(pickle.dumps(result))), 'timestamp':datetime.utcnow()}
        self.db.webpage.update({'_id':url},{'$set':record}, upsert = True)

""" class Connect(object):
    def get_connection(self):
        return MongoClient("mongodb://$[username]:$[password]@$[hostlist]/$[database]?authSource=$[authSource]") """

if __name__ == '__main__':
    cache = MongoCache(expires=timedelta())
    url = 'www.jrs.com'
    result = {'html':'hahahah'}
    cache[url] = result
    time.sleep(60)
    print cache[url]
    """ client = MongoClient('localhost',27017)
    url = 'http://example.webscraping.com/view/United-kingdom-239'
    html = '...'
    db = client.cache2 """
    """ db.webpage.insert_one(
    {
     "item": "canvas",
     "qty": 100,
     "tags": ["cotton"],
     "size": {"h": 28, "w": 35.5, "uom": "cm"}}) """
    """ cursor = db.webpage.find({})
    for item in cursor:
        pprint(item) """
    
    """ db.webpage2.insert_many([
    {"item": "journal",
     "qty": 25,
     "size": SON([("h", 14), ("w", 21), ("uom", "cm")]),
     "status": "A"},
    {"item": "notebook",
     "qty": 50,
     "size": SON([("h", 8.5), ("w", 11), ("uom", "in")]),
     "status": "A"},
    {"item": "paper",
     "qty": 100,
     "size": SON([("h", 8.5), ("w", 11), ("uom", "in")]),
     "status": "D"},
    {"item": "planner",
     "qty": 75,
     "size": SON([("h", 22.85), ("w", 30), ("uom", "cm")]),
     "status": "D"},
    {"item": "postcard",
     "qty": 45,
     "size": SON([("h", 10), ("w", 15.25), ("uom", "cm")]),
     "status": "A"}]) """
    """ cursor2 = db.webpage2.find({"status":"D"})
    cursor3 = db.webpage2.find({"size.uom":"in"})
    cursor4 = db.webpage2.find({"size.h":{"$lt":9}})#less than/greater than
    cursor5 = db.webpage2.find({"status":"A","size.h":{"$lt":9}})
    #cursor5 = db.webpage2.find({"$and":[{"status":"A"},{"size.h":{"$lt":9}}]})
    cursor6 = db.webpage2.find({"$or":[{"status":"A"},{"size.h":{"$lt":9}}]})
    cursor7 = db.webpage2.find({
        "status":"A",
        "$or":[{"qty":{"$lt":"40"}},{"item":{"$regex":"^p"}}]
    })
    print "----cursor4----"
    for item in cursor6:
        pprint(item)
    print "----cursor5----"
    for item in cursor7:
        pprint(item) """
