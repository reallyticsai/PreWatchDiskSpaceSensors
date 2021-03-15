import time
from config2.config import config
from src.dbservice.dbservicefactory import DbServiceFactory

def run():
    dbservicefactory = DbServiceFactory()
    dbservice = dbservicefactory.get_db_service()
    while(not time.sleep(5)):
        print("hello")