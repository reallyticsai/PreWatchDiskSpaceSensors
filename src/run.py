import time
from config2.config import config
from src.dbservice.dbservicefactory import DbServiceFactory
import importlib
from resources.active_plugins import plugins
import requests
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed


def generate_signal(signal_name, value):
    headers = {
        'Content-Type': 'application/json',
    }
    json = { "deployment" : { "ACD" : "Predictive", "tenantID" : "avaya" }, 
    "name" : signal_name, "__v" : 0, "level" : value, 
    "payload" : {"state": "1", "data" : [[ { "Info":"Predictive sensor" } ]] }, "signaler" : "Pre-Watch", "syncRequest":True, 
    "timestamps" : { "postTime" : round(time.time() * 1000) }
    }
    try:
        response = requests.post('http://%s:%i/signal'%(config.oversight.host,config.oversight.port), headers=headers, json=json)
    except Exception as e:
        logging.error("POST request to oversight:http://%s:%i/signal failed"%(config.oversight.host,config.oversight.port))
    
    if(response.ok):
        logging.info("Predictive Signal %s generated."%(signal_name))
        
def run(): 
    #create the db service factory
    dbservicefactory = DbServiceFactory()
    
    # create a list of plugins
    active_plugins = [
        importlib.import_module("."+plugin,"resources.plugins").Plugin(dbservicefactory) for plugin in plugins
    ]
    logging.info("Default plugins loaded")
    logging.info(plugins)

    #import external plugins
    external_plugins = config.externalplugins
    print(type(external_plugins))
    print(external_plugins)
    if(external_plugins != None and external_plugins != ""):
        external_plugins = external_plugins.split(',')
        for plugin in external_plugins:
            active_plugins.append(importlib.import_module("."+plugin,"resources.externalplugins").Plugin(dbservicefactory))
            logging.info("External plugin %s loaded"%(plugin))
    while(not time.sleep(config.interval)):
        with ThreadPoolExecutor(max_workers = config.max_threads) as executor:
            futures = {executor.submit(pg.process): pg.get_name() for pg in active_plugins}
            for future in as_completed(futures):
                signal_name = futures[future]
                value = future.result()
                generate_signal(signal_name,value.value)