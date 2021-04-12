from src.dbservice.dbservicefactory import DbServiceFactory
from statistics import mean,stdev
import json
from src.levels import Levels
import logging
import datetime

# Each new class must be named Plugin  
class Plugin:

    def __init__(self, dbservicefactory):
        # Initialization of sensor values
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
            "Name": "PREDICTIVE DATA DIRECTORY AI VM",
            "Value": 0,
            "State": "NORMAL",
            "Mean" : 0,
            "Stdev":0
            }
        self.data_historical = self.dbservice.execute_query("historicalsignaldatapoints",self.query)
        self.data_current = self.dbservice.execute_query("currentsignaldatapoints",self.query)
        self.value = round(float(self.data_current['payload'][0]['data'][0][0]['value'])) #Current Value for comparison
        self.payload['Value']=self.value
        self.start_date = datetime.date.today()
        self.data_historical['datetime'] = self.data_historical['__createdAt'].apply(lambda x: datetime.date(x.year,x.month,x.day))    
        for i in range(len(self.data_historical)):
            if(datetime.date.today()-datetime.timedelta(days=30)<=self.data_historical['datetime'][i]): #30 days old data only
                self.list1.append(round(float(self.data_historical['payload'][0]['data'][0][0]['value']))) #Append to list for mean and stdev    
        self.m = round(mean(self.list1)) # Mean of the values of historical data for the sensor
        self.payload['Mean']=self.m
        self.s = round(stdev(self.list1)) # Standard Deviation of the values of historical data for the sensor
        self.payload['Stdev']=self.s
        self.result = self.m+self.s+self.s #mean + standard deviation + 2 standard deviation
        
    #define this function to return the name of the signal (this will appear on the oversight UI)
    def get_name(self):
        return "PREDICTIVE DATA DIRECTORY AI VM"

    #define this function to return the interval that this signal must run
    def get_interval(self):
        return 60 #runs every 60 seconds or 1 minute

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
                        self.list1.append(round(float(self.data_historical['payload'][0]['data'][0][0]['value']))) #Append to list for mean and stdev
                self.m = round(mean(self.list1)) # Mean of the values of historical data for the sensor
                self.s = round(stdev(self.list1)) # Standard Deviation of the values of historical data for the sensor
                self.result = self.m+self.s+self.s #mean + standard deviation + 2 standard deviation
            else:
                self.data_current = self.dbservice.execute_query("currentsignaldatapoints",self.query)
                self.value = round(float(self.data_current['payload'][0]['data'][0][0]['value'])) #Current Value
                            
        except Exception as e:
            logging.error("Unable to execute query:",e)
        #payload2 = {}
        if self.value > self.m+self.s:
            self.payload['Name']= "PREDICTIVE DATA DIRECTORY AI VM"
            self.payload['Value']=self.value
            self.payload['State']="WARNING"
            self.payload['Mean']=self.m
            self.payload['Stdev']=self.s
            #print(self.payload)
            #payload2 = self.payload
            return Levels.WARN,self.payload#, self.payload #Warning
        elif self.value > self.result:
            self.payload['Name']="PREDICTIVE DATA DIRECTORY AI VM"
            self.payload['Value']=self.value
            self.payload['State']="ALARMED"
            self.payload['Mean']=self.m
            self.payload['Stdev']=self.s
            #print(self.payload)
            #payload2 = self.payload
            return Levels.ALARM,self.payload#, self.payload #Alarmed
        else:
            self.payload['Name']="PREDICTIVE DATA DIRECTORY AI VM"
            self.payload['Value']=self.value
            self.payload['State']="NORMAL"
            self.payload['Mean']=self.m
            self.payload['Stdev']=self.s
            #print(self.payload)
            #payload2 = self.payload
            return Levels.NORMAL,self.payload#, self.payload #Normal