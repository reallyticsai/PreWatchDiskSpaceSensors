
from src.dbservice.dbservicefactory import DbServiceFactory
from statistics import mean,stdev
import json
from src.levels import Levels
import logging
import datetime

# Each new class must be named Plugin  
class Plugin:

    def __init__(self, dbservicefactory):
        self.dbservice = dbservicefactory.get_db_service()
        self.value=0
        self.m=0
        self.s=0
        self.result=0
        self.list1 = []
        self.query = {
            "name": "DATA DIRECTORY AI VM"
        }
        self.payload = {
            "Name": "Predictive Data Directory AI VM",
            "Value": 0,
            "State": Levels.NORMAL,
            "Mean" : 0,
            "Stdev":0
            }
        self.data_historical = self.dbservice.execute_query("historicalsignaldatapoints",self.query)
        self.data_current = self.dbservice.execute_query("currentsignaldatapoints",self.query)
        self.value = self.data_current['payload'][0]['data'][0]["value"] #['value'] keyyy #Current Value
        self.payload['Value']=self.value
        self.start_date = datetime.date.today()
        self.data_historical['datetime'] = self.data_historical['__createdAt'].apply(lambda x: datetime.date(x.year,x.month,x.day))    
        for i in range(len(self.data_historical)):
            if(datetime.date.today()-datetime.timedelta(days=30)<=self.data_historical['datetime'][i]): #30 days old data only
                self.list1.append(self.data_historical['payload'][0]['data'][0]["value"]) #['value'] keyyy    
        self.m = mean(self.list1) # Mean of the values of historical data for the sensor
        self.payload['Mean']=self.m
        self.s = stdev(self.list1) # Standard Deviation of the values of historical data for the sensor
        self.payload['Stdev']=self.s
        self.result = self.m+self.s+self.s #mean + standard deviation + 2 standard deviation
        
    #define this function to return the name of the signal (this will appear on the oversight UI)
    def get_name(self):
        return "Predictive Data Directory AI VM"

    #define this function to return the interval that this signal must run
    def get_interval(self):
        return 180 #runs every 60 seconds or 1 minute

    #do all the processing here (do not rename this function)
    def process(self):

        #For more help with queries visit: https://www.w3schools.com/python/python_mongodb_query.asp

        #Fetch data into the dataframe
        try:
            if(self.start_date+datetime.timedelta(days=7)==datetime.date.today()):
                self.start_date = datetime.date.today()
                self.list1.clear()
                self.data_historical = self.dbservice.execute_query("historicalsignaldatapoints",self.query)
                self.data_historical['datetime'] = self.data_historical['__createdAt'].apply(lambda x: datetime.date(x.year,x.month,x.day))    
                for i in range(len(self.data_historical)):
                    if(datetime.date.today()-datetime.timedelta(days=30)<=self.data_historical['datetime'][i]): #30 days old data only
                        self.list1.append(self.data_historical['payload'][0]['data'][0]["value"]) #['value'] keyyy
                    
                self.m = mean(self.list1) # Mean of the values of historical data for the sensor
                self.payload['Mean']=self.m
                self.s = stdev(self.list1) # Standard Deviation of the values of historical data for the sensor
                self.payload['Stdev']=self.s
                self.result = self.m+self.s+self.s #mean + standard deviation + 2 standard deviation
            else:
                self.data_current = self.dbservice.execute_query("currentsignaldatapoints",self.query)
                self.value = self.data_current['payload'][0]['data'][0]["value"] #['value'] keyyy #Current Value
                self.payload['Value']=self.value
            
        except Exception as e:
            logging.error("Unable to execute query:",e)
        
        if self.value > self.m+self.s:
            self.payload['State']=Levels.WARN
            return Levels.WARN, self.payload #Warning WARNING not available
        elif self.value > self.result:
            self.payload['State']=Levels.ALARM
            return Levels.ALARM, self.payload #Alarmed
        else:
            self.payload['State']=Levels.NORMAL
            return Levels.NORMAL, self.payload #Normal
        # Name , Current Value, Sensor state Alarm warning or Norma, mean, standard dev