from config2.config import config

from src.dbservice.dbservicefactory import DbServiceFactory
from src.levels import Levels
import logging
from time import sleep

# Each new class must be named Plugin  
class Plugin:

    def __init__(self, dbservicefactory):
        self.dbservice = dbservicefactory.get_db_service()
    
    #define this function to return the name of the signal (this will appear on the oversight UI)
    def get_name(self):
        if(config.oversight.version == 1 or config.oversight.version == "1"):
            return "Mongo Example Prediction"
        elif (config.oversight.version == 3.1 or config.oversight.version == "3.1"):
            return "Influx v1 Example Prediction"
        elif (config.oversight.version == 3.2 or config.oversight.version == "3.2"):
            return "Influx v2 Example Prediction"
        
        return ""
    
    #define this function to return the interval that this signal must run
    def get_interval(self):
        return 60 #runs every ten seconds

    #do all the processing here (do not rename this function)
    def process(self):

        if(config.oversight.version == 1 or config.oversight.version == "1"):
            #For more help with queries visit: https://www.w3schools.com/python/python_mongodb_query.asp
            query = {
                "name": {
                    "$regex":'V6',
                    "$options":'i'
                }
            }
            table = "historicalsignaldatapoints"
        elif (config.oversight.version == 3.1 or config.oversight.version == "3.1"):
            query = "SHOW SERIES"
            table = ""
        elif (config.oversight.version == 3.2 or config.oversight.version == "3.2"):
            query = 'from(bucket:"my-bucket") |> range(start: -60m)'
            table = ''

        #Fetch data into the dataframe
        try:
            df = self.dbservice.execute_query(table, query)
        except Exception as e:
            logging.error("Unable to execute query:",e)
        #Do some magic here

        sleep(5)
        payload = {"value":15}
        
        return Levels.NORMAL,payload