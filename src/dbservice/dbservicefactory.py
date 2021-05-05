from config2.config import config
from src.dbservice.mongoservice import MongoService
from src.dbservice.influxservice import InfluxService
from src.dbservice.influx2service import Influx2Service

class DbServiceFactory:

    def __init__(self):
        if(config.oversight.version == 1 or config.oversight.version == "1"):
            self.db_service = MongoService()
        elif (config.oversight.version == 3.1 or config.oversight.version == "3.1"):
            self.db_service = InfluxService()
        elif (config.oversight.version == 3.2 or config.oversight.version == "3.2"):
            self.db_service = Influx2Service()
        else:
            raise ValueError(config.oversight.version)

    def get_db_service(self):
        return self.db_service