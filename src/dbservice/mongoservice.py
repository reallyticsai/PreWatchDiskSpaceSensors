from src.dbservice.dbserviceinterface import DbServiceInterface
from config2.config import config
from pandas import DataFrame
import pymongo
import ast

class MongoService(DbServiceInterface):

    def __init__(self):
        print("In mongo service const")
        auth_section = config.mongo.user+':'+config.mongo.password+'@'
        mongo_uri = "mongodb://%s%s:%s" % (auth_section,config.mongo.host,config.mongo.port)
        print(mongo_uri)
        self.client = pymongo.MongoClient(mongo_uri)
        self.db = self.client[config.mongo.db]

    def execute_query(self, table, query_str):
        collection = self.db[table]
        query = ast.literal_eval(query_str)
        result = collection.find(query)
        df = DataFrame(list(result))
        return df