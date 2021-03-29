from src.dbservice.dbserviceinterface import DbServiceInterface
from config2.config import config
from pandas import DataFrame
import pymongo
import ast
import logging

class MongoService(DbServiceInterface):

    def __init__(self):
        auth_section = config.mongo.user+':'+config.mongo.password+'@'
        mongo_uri = "mongodb://%s%s:%s" % (auth_section,config.mongo.host,config.mongo.port)
        try:
            self.client = pymongo.MongoClient(mongo_uri)
            self.db = self.client[config.mongo.db]
        except Exception as exc:
            logging.error('Unable to connect to mongo db at  %s:%s. \nException: %s' % (config.mongo.host,config.mongo.port,exc))

    def execute_query(self, table, query):
        df = {}
        try:
            collection = self.db[table]
            result = collection.find(query)
            df = DataFrame(list(result))
        except Exception as exc:
            logging.error('Unable to execute query: %s \nException: %s' % (query,exc))
        return df