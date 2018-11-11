# -*- coding: utf-8 -*-
import os
from pymongo import MongoClient
from pprint import pprint
from bson.son import SON

class Connect(object):
    def get_connection(self):
        return MongoClient("mongodb://$[username]:$[password]@$[hostlist]/$[database]?authSource=$[authSource]")

if __name__ == "__main__":
    client = MongoClient('localhost',27017)
    url = 'http://example.webscraping.com/view/United-kingdom-239'
    html = '...'
    db = client.cache
    db.webpage.insert_one(
    {
     "item": "canvas",
     "qty": 100,
     "tags": ["cotton"],
     "size": {"h": 28, "w": 35.5, "uom": "cm"}})
    cursor = db.webpage.find({})
    for item in cursor:
        pprint(item)
    
    db.webpage2.insert_many([
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
     "status": "A"}])
    cursor2 = db.webpage2.find({"status":"D"})

    for item in cursor2:
        pprint(item)
