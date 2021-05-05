import argparse
from src.dbservice.dbserviceinterface import DbServiceInterface
from pandas import DataFrame
from config2.config import config

from influxdb_client import InfluxDBClient

class Influx2Service(DbServiceInterface):

    def __init__(self):
        host = config.influx2.host
        port = config.influx2.port
        token = config.influx2.token
        org = config.influx2.org
        
        try:
            self.client = InfluxDBClient(url=f'http://{host}:{port}', token=token, org=org)
        except Exception as e:
            print(f'Unable to connect to InfluxDB Client. Exception: {e}')

    def execute_query(self, table, query):
        df = {}
        query_api = self.client.query_api()

        try:
            df = query_api.query_data_frame(query)
        except Exception as e:
            print(f'Unable to query to InfluxDB Client. Exception: {e}')
            
        return df