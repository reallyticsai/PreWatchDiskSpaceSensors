from config2.config import config
from src.dbservice.mongoservice import MongoService

class DbServiceFactory:

    def __init__(self):
        if(config.oversight.version == 1 or config.oversight.version == "1"):
            self.db_service = MongoService()
        else:
            raise ValueError(config.oversight.version)

    def get_db_service(self):
        return self.db_service