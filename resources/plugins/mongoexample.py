
from src.dbservice.dbservicefactory import DbServiceFactory
from src.levels import Levels
import logging

# Each new class must be named Plugin  
class Plugin:

    def __init__(self, dbservicefactory):
        self.dbservice = dbservicefactory.get_db_service()
    
    #define this function to return the name of the signal (this will appear on the oversight UI)
    def get_name(self):
        return "Mongo Example Prediction"

    #do all the processing here (do not rename this function)
    def process(self):

        #For more help with queries visit: https://www.w3schools.com/python/python_mongodb_query.asp
        query = {
            "name": {
                "$regex":'V6',
                "$options":'i'
            }
        }
        #Fetch data into the dataframe
        try:
            df = self.dbservice.execute_query("historicalsignaldatapoints",query)
        except Exception as e:
            logging.error("Unable to execute query:",e)
        #Do some magic here
        
        return Levels.NORMAL