from src.dbservice.dbserviceinterface import DbServiceInterface
class MongoService(DbServiceInterface):

    def __init__(self):
        print("In mongo service const")
        #TODO: establish connection here
        
    def execute_query(self, query_str):
        print("Executing query")
