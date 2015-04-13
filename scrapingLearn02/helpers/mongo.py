__author__ = 'enapiuz'

import pymongo
from pymongo.errors import DuplicateKeyError

# TODO сделать из этого класс, конструктор которого принимает имя базы и, возможно, коллекцию для удобства

client = pymongo.MongoClient("localhost", 27017)
db = client.testgrab
collection = db.test2collection
collection.create_index("url", unique=True)


# TODO нормально починить индекс
def save_entry(entry):
    try:
        return collection.insert_one(entry).inserted_id
    except DuplicateKeyError as e:
        return -1