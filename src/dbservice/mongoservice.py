from src.dbservice.dbserviceinterface import DbServiceInterface
from config2.config import config
from pandas import DataFrame
import pymongo
import ast

class MongoService(DbServiceInterface):

    def __init__(self):
        auth_section = config.mongo.user+':'+config.mongo.password+'@'
        mongo_uri = "mongodb://%s%s:%s" % (auth_section,config.mongo.host,config.mongo.port)
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[config.mongo.db]

    def execute_query(self, table, query):
        collection = self.db[table]
        result = collection.find(query)
        df = DataFrame(list(result))
        return df