
from src.dbservice.dbservicefactory import DbServiceFactory
from src.levels import Levels
import logging

# Each new class must be named Plugin  
class Plugin:

    def __init__(self, dbservicefactory):
        self.dbservice = dbservicefactory.get_db_service()
    
    #define this function to return the name of the signal (this will appear on the oversight UI)
    def get_name(self):
        return "Predictive Data Directory AI VM"

    #do all the processing here (do not rename this function)
    def process(self):

        #For more help with queries visit: https://www.w3schools.com/python/python_mongodb_query.asp
        query = {
            "name": "DATA DIRECTORY AI VM"
        }
        #Fetch data into the dataframe
        try:
            data_historical = self.dbservice.execute_query("historicalsignaldatapoints",query)
            data_current = self.dbservice.execute_query("currentsignaldatapoints",query)
        except Exception as e:
            logging.error("Unable to execute query:",e)
        #Do some magic here
        m = mean(data_historical.payload.data.value); # Mean of the values of historical data for the sensor
        s = stddev(data_historical.payload.data.value); # Standard Deviation of the values of historical data for the sensor
        result = m+s+(2*s); #mean + standard deviation + 2 standard deviation
        # mean+std+2std for the past 45 days historical data
        if data_current.payload.data.value > 80 and data_current.payload.data.value < 85:
            return Levels.WARNING; #Warning
        elif data_current.payload.data.value < m or data_current.payload.data.value < 80:
            return Levels.NORMAL; #Normal
        return Levels.ALARM; #Alarmed