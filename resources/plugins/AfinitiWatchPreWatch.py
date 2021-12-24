import psycopg2
import time
from statsmodels.tsa.ar_model import AutoReg
from statistics import mean,stdev
import pandas as pd
import datetime
from datetime import date
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

class PreWatch():
    def __init__(self):
        self.connection=[]
        self.cpuLoadSensors = list()
        self.cpuUsageSensors = list()
        self.dataUsageSensors = list()
        self.ramUsageSensors = list()
        self.rootUsageSensors = list()
        self.ioLoadSensors = list()
        self.cursor = []
        self.value=0
        self.m=0
        self.s=0
        self.result=0
        self.r1=0
        self.r2=0
        self.sum=0
        self.exp = ""
        self.list1 = []
        self.record = []
        self.cpuLoadSensorsDf = pd.DataFrame(columns = ['Timestamp','Sensor','Current Value','Mean','Standard Dev','Result','Expected Value','Flag'])
        self.cpuUsageSensorsDf = pd.DataFrame(columns = ['Timestamp','Sensor','Current Value','Mean','Standard Dev','Result','Expected Value','Flag'])
        self.dataUsageSensorsDf = pd.DataFrame(columns = ['Timestamp','Sensor','Current Value','Mean','Standard Dev','Result','Expected Value','Flag'])
        self.ramUsageSensorsDf = pd.DataFrame(columns = ['Timestamp','Sensor','Current Value','Mean','Standard Dev','Result','Expected Value','Flag'])
        self.rootUsageSensorsDf = pd.DataFrame(columns = ['Timestamp','Sensor','Current Value','Mean','Standard Dev','Result','Expected Value','Flag'])
        self.ioLoadSensorsDf = pd.DataFrame(columns = ['Timestamp','Sensor','Current Value','Mean','Standard Dev','Result','Expected Value','Flag'])
        self.engine = create_engine('postgresql://postgres:admin@10.136.68.29:5438/postgres')
        self.start_date = date.today()
        try:
            self.cpuLoadSensorsDf.to_sql('cpuLoadPredictive', self.engine,index=False)
        except:
                pass
        try:
            self.cpuUsageSensorsDf.to_sql('cpuUsagePredictive', self.engine,index=False)
        except:
            pass
        try:
            self.dataUsageSensorsDf.to_sql('dataUsagePredictive', self.engine,index=False)
        except:
            pass
        try:
            self.ramUsageSensorsDf.to_sql('ramUsagePredictive', self.engine,index=False)
        except:
            pass
        try:
            self.rootUsageSensorsDf.to_sql('rootUsagePredictive', self.engine,index=False)
        except:
            pass
        try:
            self.ioLoadSensorsDf.to_sql('ioLoadPredictive', self.engine,index=False)
        except:
            pass
        self.create_connection()
        self.meCPU = []
        self.stCPU = []
        self.resCPU = []
        self.exCPU = []
        valuesCPULoad=[]
        self.recordCPULoad = []
        for i in range(len(self.cpuLoadSensors)):
            sensor = str(self.cpuLoadSensors[i])
            s = 'SELECT "'
            s = s + sensor+'-value" from public."'
            s = s + sensor
            s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
            s = s + "'30' day ;"
            b=[]
            self.cursor.execute(s)
            a = self.cursor.fetchall()
            
            for j in range(len(a)):
                b.append(float(a[j][0]))
            self.recordCPULoad.append(b)
            
            s = 'SELECT "'
            s = s + str(self.cpuLoadSensors[i])+'-value" from public."'
            s = s + str(self.cpuLoadSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesCPULoad.append(a[0])
        
            m,std,resul,exp = self.modelRun(self.recordCPULoad[i])
            self.meCPU.append(m)
            self.stCPU.append(std)
            self.resCPU.append(resul)
            self.exCPU.append(exp)
            if self.value >= self.meCPU[i]+self.stCPU[i] and self.value < self.resCPU[i]:
                flag = -1 #Warning
            elif self.value >= self.resCPU[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            s = ''
            s = 'INSERT INTO public."cpuLoadPredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
            s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
            self.cursor.execute(s)
            self.connection.commit()
        self.mecpuUsage = []
        self.stcpuUsage = []
        self.rescpuUsage = []
        self.excpuUsage = []
        valuescpuUsage=[]
        self.recordcpuUsage = []
        for i in range(len(self.cpuUsageSensors)):
            sensor = str(self.cpuUsageSensors[i])
            s = 'SELECT "'
            s = s + sensor+'-value" from public."'
            s = s + sensor
            s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
            s = s + "'30' day ;"
            b=[]
            self.cursor.execute(s)
            a = self.cursor.fetchall()

            for j in range(len(a)):
                b.append(float(a[j][0]))
            self.recordcpuUsage.append(b)

            s = 'SELECT "'
            s = s + str(self.cpuUsageSensors[i])+'-value" from public."'
            s = s + str(self.cpuUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuescpuUsage.append(a[0])

            m,std,resul,exp = self.modelRun(self.recordcpuUsage[i])
            self.mecpuUsage.append(m)
            self.stcpuUsage.append(std)
            self.rescpuUsage.append(resul)
            self.excpuUsage.append(exp)
            if self.value >= self.mecpuUsage[i]+self.stcpuUsage[i] and self.value < self.rescpuUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.rescpuUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            s = ''
            s = 'INSERT INTO public."cpuUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
            s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
            self.cursor.execute(s)
            self.connection.commit()      
        self.medataUsage = []
        self.stdataUsage = []
        self.resdataUsage = []
        self.exdataUsage = []
        valuesdataUsage=[]
        self.recorddataUsage = []
        for i in range(len(self.dataUsageSensors)):
            sensor = str(self.dataUsageSensors[i])
            s = 'SELECT "'
            s = s + sensor+'-value" from public."'
            s = s + sensor
            s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
            s = s + "'30' day ;"
            b=[]
            self.cursor.execute(s)
            a = self.cursor.fetchall()

            for j in range(len(a)):
                b.append(float(a[j][0]))
            self.recorddataUsage.append(b)

            s = 'SELECT "'
            s = s + str(self.dataUsageSensors[i])+'-value" from public."'
            s = s + str(self.dataUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesdataUsage.append(a[0])

            m,std,resul,exp = self.modelRun(self.recorddataUsage[i])
            self.medataUsage.append(m)
            self.stdataUsage.append(std)
            self.resdataUsage.append(resul)
            self.exdataUsage.append(exp)
            if self.value >= self.medataUsage[i]+self.stdataUsage[i] and self.value < self.resdataUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.resdataUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            s = ''
            s = 'INSERT INTO public."dataUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
            s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
            self.cursor.execute(s)
            self.connection.commit()
        self.meramUsage = []
        self.stramUsage = []
        self.resramUsage = []
        self.exramUsage = []
        valuesramUsage=[]
        self.recordramUsage = []
        for i in range(len(self.ramUsageSensors)):
            sensor = str(self.ramUsageSensors[i])
            s = 'SELECT "'
            s = s + sensor+'-value" from public."'
            s = s + sensor
            s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
            s = s + "'30' day ;"
            b=[]
            self.cursor.execute(s)
            a = self.cursor.fetchall()

            for j in range(len(a)):
                b.append(float(a[j][0]))
            self.recordramUsage.append(b)

            s = 'SELECT "'
            s = s + str(self.ramUsageSensors[i])+'-value" from public."'
            s = s + str(self.ramUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesramUsage.append(a[0])

            m,std,resul,exp = self.modelRun(self.recordramUsage[i])
            self.meramUsage.append(m)
            self.stramUsage.append(std)
            self.resramUsage.append(resul)
            self.exramUsage.append(exp)
            if self.value >= self.meramUsage[i]+self.stramUsage[i] and self.value < self.resramUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.resramUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            s = ''
            s = 'INSERT INTO public."ramUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
            s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
            self.cursor.execute(s)
            self.connection.commit()
        self.merootUsage = []
        self.strootUsage = []
        self.resrootUsage = []
        self.exrootUsage = []
        valuesrootUsage=[]
        self.recordrootUsage = []
        for i in range(len(self.rootUsageSensors)):
            sensor = str(self.rootUsageSensors[i])
            s = 'SELECT "'
            s = s + sensor+'-value" from public."'
            s = s + sensor
            s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
            s = s + "'30' day ;"
            b=[]
            self.cursor.execute(s)
            a = self.cursor.fetchall()

            for j in range(len(a)):
                b.append(float(a[j][0]))
            self.recordrootUsage.append(b)

            s = 'SELECT "'
            s = s + str(self.rootUsageSensors[i])+'-value" from public."'
            s = s + str(self.rootUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesrootUsage.append(a[0])

            m,std,resul,exp = self.modelRun(self.recordrootUsage[i])
            self.merootUsage.append(m)
            self.strootUsage.append(std)
            self.resrootUsage.append(resul)
            self.exrootUsage.append(exp)
            if self.value >= self.merootUsage[i]+self.strootUsage[i] and self.value < self.resrootUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.resrootUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            s = ''
            s = 'INSERT INTO public."rootUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
            s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
            self.cursor.execute(s)
            self.connection.commit()
        self.meioLoad = []
        self.stioLoad = []
        self.resioLoad = []
        self.exioLoad = []
        valuesioLoad=[]
        self.recordioLoad = []
        for i in range(len(self.ioLoadSensors)):
            sensor = str(self.ioLoadSensors[i])
            s = 'SELECT "'
            s = s + sensor+'-value" from public."'
            s = s + sensor
            s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
            s = s + "'30' day ;"
            b=[]
            self.cursor.execute(s)
            a = self.cursor.fetchall()

            for j in range(len(a)):
                b.append(float(a[j][0]))
            self.recordioLoad.append(b)

            s = 'SELECT "'
            s = s + str(self.ioLoadSensors[i])+'-value" from public."'
            s = s + str(self.ioLoadSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesioLoad.append(a[0])

            m,std,resul,exp = self.modelRun(self.recordioLoad[i])
            self.meioLoad.append(m)
            self.stioLoad.append(std)
            self.resioLoad.append(resul)
            self.exioLoad.append(exp)
            if self.value >= self.meioLoad[i]+self.stioLoad[i] and self.value < self.resioLoad[i]:
                flag = -1 #Warning
            elif self.value >= self.resioLoad[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            s = ''
            s = 'INSERT INTO public."ioLoadPredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
            s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
            self.cursor.execute(s)
            self.connection.commit()         
           
    def create_connection(self):
        try:
            self.connection = psycopg2.connect(user = "postgres",
                                      password = "admin",
                                      host = "10.136.68.29",
                                      port = "5438",
                                      database = "postgres")
            
            self.cursor = self.connection.cursor()

            # Retrieve all the rows from the cursor
            self.cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
            for table in self.cursor.fetchall():
                if 'cpuload' in table[0].lower() and 'predictive' not in table[0].lower():
                    self.cpuLoadSensors.append(table[0])
                if 'cpuusage' in table[0].lower() and 'predictive' not in table[0].lower():
                    self.cpuUsageSensors.append(table[0])
                if 'datausage' in table[0].lower() and 'predictive' not in table[0].lower():
                    self.dataUsageSensors.append(table[0])
                if 'ramusage' in table[0].lower() and 'predictive' not in table[0].lower():
                    self.ramUsageSensors.append(table[0])
                if 'rootusage' in table[0].lower() and 'predictive' not in table[0].lower():
                    self.rootUsageSensors.append(table[0])
                if 'ioload' in table[0].lower() and 'predictive' not in table[0].lower():
                    self.ioLoadSensors.append(table[0])

        except (Exception, psycopg2.Error) as error :
            print ("Error while connecting to PostgreSQL", error)

    def cpuSensors(self):
        valuesCPULoad=[]
        self.recordCPULoad = []
        for i in range(len(self.cpuLoadSensors)):
            
            sensor = str(self.cpuLoadSensors[i])
            s = 'SELECT "'
            s = s + str(self.cpuLoadSensors[i])+'-value" from public."'
            s = s + str(self.cpuLoadSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesCPULoad.append(a[0])
            if(self.start_date+datetime.timedelta(days=7)==date.today()):
                self.start_date = date.today()
                m,std,resul,exp = self.modelRun(self.recordCPULoad[i])
                self.meCPU.clear()
                self.stCPU.clear()
                self.resCPU.clear()
                self.exCPU.clear()
                self.meCPU.append(m)
                self.stCPU.append(std)
                self.resCPU.append(resul)
                self.exCPU.append(exp)
                for j in range(len(self.cpuLoadSensors)):
                    sensor = str(self.cpuLoadSensors[j])
                    s = 'SELECT "'
                    s = s + sensor+'-value" from public."'
                    s = s + sensor
                    s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
                    s = s + "'30' day ;"
                    b=[]
                    self.cursor.execute(s)
                    a = self.cursor.fetchall()
                    s = 'SELECT "'
                    s = s + str(self.cpuLoadSensors[j])+'-value" from public."'
                    s = s + str(self.cpuLoadSensors[j])
                    s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
                    self.cursor.execute(s)
                    a = self.cursor.fetchone()
                    valuesCPULoad.append(a[0])
                    for k in range(len(a)):
                        b.append(float(a[k][0]))
                    self.recordCPULoad.append(b)
                    if self.value >= self.meCPU[j]+self.stCPU[j] and self.value < self.resCPU[j]:
                        flag = -1 #Warning
                    elif self.value >= self.resCPU[j]:
                        flag = 1 #Alarmed
                    else:
                        flag = 0 #Normal
                    
                    s = ''
                    s = 'INSERT INTO public."cpuLoadPredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
                    s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
                    self.cursor.execute(s)
                    self.connection.commit()
            
            if self.value >= self.meCPU[i]+self.stCPU[i] and self.value < self.resCPU[i]:
                flag = -1 #Warning
            elif self.value >= self.resCPU[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            
            s = ''
            s = 'UPDATE public."cpuLoadPredictive" SET "Timestamp"='+"'"+str(date.today())+"', "+'"Current Value"='+str(a[0])+", "+'"Flag"='+str(flag)+ ' WHERE "Sensor"='+"'"+str(sensor)+"'"+';'
            self.cursor.execute(s)
            self.connection.commit()
            
    def cpuUsage(self):
        valuescpuUsage=[]
        self.recordcpuUsage = []
        for i in range(len(self.cpuUsageSensors)):
            
            sensor = str(self.cpuUsageSensors[i])
            s = 'SELECT "'
            s = s + str(self.cpuUsageSensors[i])+'-value" from public."'
            s = s + str(self.cpuUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuescpuUsage.append(a[0])
            if(self.start_date+datetime.timedelta(days=7)==date.today()):
                self.start_date = date.today()
                m,std,resul,exp = self.modelRun(self.recordcpuUsage[i])
                self.mecpuUsage.clear()
                self.stcpuUsage.clear()
                self.rescpuUsage.clear()
                self.excpuUsage.clear()
                self.mecpuUsage.append(m)
                self.stcpuUsage.append(std)
                self.rescpuUsage.append(resul)
                self.excpuUsage.append(exp)
                for j in range(len(self.cpuUsageSensors)):
                    sensor = str(self.cpuUsageSensors[j])
                    s = 'SELECT "'
                    s = s + sensor+'-value" from public."'
                    s = s + sensor
                    s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
                    s = s + "'30' day ;"
                    b=[]
                    self.cursor.execute(s)
                    a = self.cursor.fetchall()
                    s = 'SELECT "'
                    s = s + str(self.cpuUsageSensors[j])+'-value" from public."'
                    s = s + str(self.cpuUsageSensors[j])
                    s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
                    self.cursor.execute(s)
                    a = self.cursor.fetchone()
                    valuescpuUsage.append(a[0])
                    for k in range(len(a)):
                        b.append(float(a[k][0]))
                    self.recordcpuUsage.append(b)
                    if self.value >= self.mecpuUsage[j]+self.stcpuUsage[j] and self.value < self.rescpuUsage[j]:
                        flag = -1 #Warning
                    elif self.value >= self.rescpuUsage[j]:
                        flag = 1 #Alarmed
                    else:
                        flag = 0 #Normal
                    
                    s = ''
                    s = 'INSERT INTO public."cpuUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
                    s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
                    self.cursor.execute(s)
                    self.connection.commit()
            
            if self.value >= self.mecpuUsage[i]+self.stcpuUsage[i] and self.value < self.rescpuUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.rescpuUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            
            s = ''
            s = 'UPDATE public."cpuUsagePredictive" SET "Timestamp"='+"'"+str(date.today())+"', "+'"Current Value"='+str(a[0])+", "+'"Flag"='+str(flag)+ ' WHERE "Sensor"='+"'"+str(sensor)+"'"+';'
            self.cursor.execute(s)
            self.connection.commit()       

    def dataUsage(self):
        valuesdataUsage=[]
        self.recorddataUsage = []
        for i in range(len(self.dataUsageSensors)):
            
            sensor = str(self.dataUsageSensors[i])
            s = 'SELECT "'
            s = s + str(self.dataUsageSensors[i])+'-value" from public."'
            s = s + str(self.dataUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesdataUsage.append(a[0])
            if(self.start_date+datetime.timedelta(days=7)==date.today()):
                self.start_date = date.today()
                m,std,resul,exp = self.modelRun(self.recorddataUsage[i])
                self.medataUsage.clear()
                self.stdataUsage.clear()
                self.resdataUsage.clear()
                self.exdataUsage.clear()
                self.medataUsage.append(m)
                self.stdataUsage.append(std)
                self.resdataUsage.append(resul)
                self.exdataUsage.append(exp)
                for j in range(len(self.dataUsageSensors)):
                    sensor = str(self.dataUsageSensors[j])
                    s = 'SELECT "'
                    s = s + sensor+'-value" from public."'
                    s = s + sensor
                    s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
                    s = s + "'30' day ;"
                    b=[]
                    self.cursor.execute(s)
                    a = self.cursor.fetchall()
                    s = 'SELECT "'
                    s = s + str(self.dataUsageSensors[j])+'-value" from public."'
                    s = s + str(self.dataUsageSensors[j])
                    s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
                    self.cursor.execute(s)
                    a = self.cursor.fetchone()
                    valuesdataUsage.append(a[0])
                    for k in range(len(a)):
                        b.append(float(a[k][0]))
                    self.recorddataUsage.append(b)
                    if self.value >= self.medataUsage[j]+self.stdataUsage[j] and self.value < self.resdataUsage[j]:
                        flag = -1 #Warning
                    elif self.value >= self.resdataUsage[j]:
                        flag = 1 #Alarmed
                    else:
                        flag = 0 #Normal
                    
                    s = ''
                    s = 'INSERT INTO public."dataUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
                    s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
                    self.cursor.execute(s)
                    self.connection.commit()
            
            if self.value >= self.medataUsage[i]+self.stdataUsage[i] and self.value < self.resdataUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.resdataUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            
            s = ''
            s = 'UPDATE public."dataUsagePredictive" SET "Timestamp"='+"'"+str(date.today())+"', "+'"Current Value"='+str(a[0])+", "+'"Flag"='+str(flag)+ ' WHERE "Sensor"='+"'"+str(sensor)+"'"+';'
            self.cursor.execute(s)
            self.connection.commit()
    
    def ramUsage(self):
        valuesramUsage=[]
        self.recordramUsage = []
        for i in range(len(self.ramUsageSensors)):
            
            sensor = str(self.ramUsageSensors[i])
            s = 'SELECT "'
            s = s + str(self.ramUsageSensors[i])+'-value" from public."'
            s = s + str(self.ramUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesramUsage.append(a[0])
            if(self.start_date+datetime.timedelta(days=7)==date.today()):
                self.start_date = date.today()
                m,std,resul,exp = self.modelRun(self.recordramUsage[i])
                self.meramUsage.clear()
                self.stramUsage.clear()
                self.resramUsage.clear()
                self.exramUsage.clear()
                self.meramUsage.append(m)
                self.stramUsage.append(std)
                self.resramUsage.append(resul)
                self.exramUsage.append(exp)
                for j in range(len(self.ramUsageSensors)):
                    sensor = str(self.ramUsageSensors[j])
                    s = 'SELECT "'
                    s = s + sensor+'-value" from public."'
                    s = s + sensor
                    s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
                    s = s + "'30' day ;"
                    b=[]
                    self.cursor.execute(s)
                    a = self.cursor.fetchall()
                    s = 'SELECT "'
                    s = s + str(self.ramUsageSensors[j])+'-value" from public."'
                    s = s + str(self.ramUsageSensors[j])
                    s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
                    self.cursor.execute(s)
                    a = self.cursor.fetchone()
                    valuesramUsage.append(a[0])
                    for k in range(len(a)):
                        b.append(float(a[k][0]))
                    self.recordramUsage.append(b)
                    if self.value >= self.meramUsage[j]+self.stramUsage[j] and self.value < self.resramUsage[j]:
                        flag = -1 #Warning
                    elif self.value >= self.resramUsage[j]:
                        flag = 1 #Alarmed
                    else:
                        flag = 0 #Normal
                    
                    s = ''
                    s = 'INSERT INTO public."ramUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
                    s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
                    self.cursor.execute(s)
                    self.connection.commit()
            
            if self.value >= self.meramUsage[i]+self.stramUsage[i] and self.value < self.resramUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.resramUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            
            s = ''
            s = 'UPDATE public."ramUsagePredictive" SET "Timestamp"='+"'"+str(date.today())+"', "+'"Current Value"='+str(a[0])+", "+'"Flag"='+str(flag)+ ' WHERE "Sensor"='+"'"+str(sensor)+"'"+';'
            self.cursor.execute(s)
            self.connection.commit()
        
    def rootUsage(self):
        valuesrootUsage=[]
        self.recordrootUsage = []
        for i in range(len(self.rootUsageSensors)):
            sensor = str(self.rootUsageSensors[i])
            s = 'SELECT "'
            s = s + str(self.rootUsageSensors[i])+'-value" from public."'
            s = s + str(self.rootUsageSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesrootUsage.append(a[0])
            if(self.start_date+datetime.timedelta(days=7)==date.today()):
                self.start_date = date.today()
                m,std,resul,exp = self.modelRun(self.recordrootUsage[i])
                self.merootUsage.clear()
                self.strootUsage.clear()
                self.resrootUsage.clear()
                self.exrootUsage.clear()
                self.merootUsage.append(m)
                self.strootUsage.append(std)
                self.resrootUsage.append(resul)
                self.exrootUsage.append(exp)
                for j in range(len(self.rootUsageSensors)):
                    sensor = str(self.rootUsageSensors[j])
                    s = 'SELECT "'
                    s = s + sensor+'-value" from public."'
                    s = s + sensor
                    s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
                    s = s + "'30' day ;"
                    b=[]
                    self.cursor.execute(s)
                    a = self.cursor.fetchall()
                    s = 'SELECT "'
                    s = s + str(self.rootUsageSensors[j])+'-value" from public."'
                    s = s + str(self.rootUsageSensors[j])
                    s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
                    self.cursor.execute(s)
                    a = self.cursor.fetchone()
                    valuesrootUsage.append(a[0])
                    for k in range(len(a)):
                        b.append(float(a[k][0]))
                    self.recordrootUsage.append(b)
                    if self.value >= self.merootUsage[j]+self.strootUsage[j] and self.value < self.resrootUsage[j]:
                        flag = -1 #Warning
                    elif self.value >= self.resrootUsage[j]:
                        flag = 1 #Alarmed
                    else:
                        flag = 0 #Normal
                    
                    s = ''
                    s = 'INSERT INTO public."rootUsagePredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
                    s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
                    self.cursor.execute(s)
                    self.connection.commit()
            
            if self.value >= self.merootUsage[i]+self.strootUsage[i] and self.value < self.resrootUsage[i]:
                flag = -1 #Warning
            elif self.value >= self.resrootUsage[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            
            s = ''
            s = 'UPDATE public."rootUsagePredictive" SET "Timestamp"='+"'"+str(date.today())+"', "+'"Current Value"='+str(a[0])+", "+'"Flag"='+str(flag)+ ' WHERE "Sensor"='+"'"+str(sensor)+"'"+';'
            self.cursor.execute(s)
            self.connection.commit()
        
    def ioLoad(self):
        valuesioLoad=[]
        self.recordioLoad = []
        for i in range(len(self.ioLoadSensors)):
            
            sensor = str(self.ioLoadSensors[i])
            s = 'SELECT "'
            s = s + str(self.ioLoadSensors[i])+'-value" from public."'
            s = s + str(self.ioLoadSensors[i])
            s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
            self.cursor.execute(s)
            a = self.cursor.fetchone()
            valuesioLoad.append(a[0])
            if(self.start_date+datetime.timedelta(days=7)==date.today()):
                self.start_date = date.today()
                m,std,resul,exp = self.modelRun(self.recordioLoad[i])
                self.meioLoad.clear()
                self.stioLoad.clear()
                self.resioLoad.clear()
                self.exioLoad.clear()
                self.meioLoad.append(m)
                self.stioLoad.append(std)
                self.resioLoad.append(resul)
                self.exioLoad.append(exp)
                for j in range(len(self.ioLoadSensors)):
                    sensor = str(self.ioLoadSensors[j])
                    s = 'SELECT "'
                    s = s + sensor+'-value" from public."'
                    s = s + sensor
                    s = s + '" WHERE timestamp > CURRENT_DATE - INTERVAL '
                    s = s + "'30' day ;"
                    b=[]
                    self.cursor.execute(s)
                    a = self.cursor.fetchall()
                    s = 'SELECT "'
                    s = s + str(self.ioLoadSensors[j])+'-value" from public."'
                    s = s + str(self.ioLoadSensors[j])
                    s = s + '" WHERE timestamp > CURRENT_DATE order by timestamp desc;'
                    self.cursor.execute(s)
                    a = self.cursor.fetchone()
                    valuesioLoad.append(a[0])
                    for k in range(len(a)):
                        b.append(float(a[k][0]))
                    self.recordioLoad.append(b)
                    if self.value >= self.meioLoad[j]+self.stioLoad[j] and self.value < self.resioLoad[j]:
                        flag = -1 #Warning
                    elif self.value >= self.resioLoad[j]:
                        flag = 1 #Alarmed
                    else:
                        flag = 0 #Normal
                    
                    s = ''
                    s = 'INSERT INTO public."ioLoadPredictive"("Timestamp", "Sensor", "Current Value", "Mean", "Standard Dev", "Result", "Expected Value", "Flag")'
                    s = s + " values ("+"'"+str(date.today())+"'"+", "+"'"+str(sensor)+"'"+", "+str(a[0])+", "+str(m)+", "+str(std)+", "+str(resul)+", "+"'"+str(exp)+"'"+", "+str(flag)+");"
                    self.cursor.execute(s)
                    self.connection.commit()
            
            if self.value >= self.meioLoad[i]+self.stioLoad[i] and self.value < self.resioLoad[i]:
                flag = -1 #Warning
            elif self.value >= self.resioLoad[i]:
                flag = 1 #Alarmed
            else:
                flag = 0 #Normal
            
            s = ''
            s = 'UPDATE public."ioLoadPredictive" SET "Timestamp"='+"'"+str(date.today())+"', "+'"Current Value"='+str(a[0])+", "+'"Flag"='+str(flag)+ ' WHERE "Sensor"='+"'"+str(sensor)+"'"+';'
            self.cursor.execute(s)
            self.connection.commit()
        
    def modelRun(self,list1):
        self.X_train = list1
        model = AutoReg(self.X_train,lags=180).fit()
        self.pred_future = model.predict(start=len(list1)+1,end=len(list1)+10080) #7days
        self.s =  round(stdev(list1),4)
        # For Future Dates
        self.m = round(mean(self.pred_future),4) # Mean of the values of historical data for the sensor
        self.sum = round(self.m-self.s-self.s,4)
        if(self.sum<=0):
            self.sum = 0
        self.r1 = str(self.sum)
        self.sum = 0
        self.sum = round(self.m+self.s+self.s,4)
        if(self.sum>=100):
            self.sum = 90
        self.r2 = str(self.sum)
        self.exp = self.r1 +" - "+ self.r2
        self.result = round(self.m+self.s+self.s,4)
        if(self.result>=100):
            self.result = 90
        elif(self.result<=0):
            self.result = 0
        return self.m,self.s,self.result,self.exp

    def RunWatch(self):
        while True:
            try:
                self.cpuSensors()
                self.cpuUsage()
                self.dataUsage()
                self.ramUsage()
                self.rootUsage()
                self.ioLoad()
            except Exception as ex:
                print(ex)
                print('Contact Sheikh Muhammad Qasim sheikh.qasim@afiniti.com OR +923054129775')

PW = PreWatch()
PW.RunWatch()