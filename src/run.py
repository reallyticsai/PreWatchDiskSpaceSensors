import time
from config2.config import config


def run():
    while(not time.sleep(5)):
        print("hello ",config.oversight.version)