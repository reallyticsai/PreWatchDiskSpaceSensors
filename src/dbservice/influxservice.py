import argparse
from src.dbservice.dbserviceinterface import DbServiceInterface
from pandas import DataFrame
from config2.config import config

from influxdb import InfluxDBClient

class InfluxService(DbServiceInterface):

    def __init__(self):
        host = config.influx.host
        port = config.influx.port
        user = config.influx.user
        password = config.influx.password
        db = config.influx.db

        try:
            self.client = InfluxDBClient(host, port, user, password, db)
        except Exception as e:
            print(f'Unable to connect to InfluxDB Client. Exception: {e}')

    def execute_query(self, table, query):
        df = {}

        try:
            result = self.client.query(query)
            df = DataFrame(list(result))
        except Exception as e:
            print(f'Unable to query to InfluxDB Client. Exception: {e}')
            
        return df
        