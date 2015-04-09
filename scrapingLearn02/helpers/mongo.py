__author__ = 'enapiuz'

import pymongo

# TODO сделать из этого класс, конструктор которого принимает имя базы и, возможно, коллекцию для удобства

client = pymongo.MongoClient("localhost", 27017)
db = client.testgrab