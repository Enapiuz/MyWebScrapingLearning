__author__ = 'enapiuz'

import pymongo

client = pymongo.MongoClient("localhost", 27017)
db = client.testgrab
collection = db.testhrefcollection
collection.create_index("href", unique=True)


def save_entry(entry):
    return collection.insert_one(entry).inserted_id


def get_entries():
    return collection.find({})