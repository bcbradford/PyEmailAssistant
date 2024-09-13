''' Main script used as app entry point '''

import os
from pyemailassistant.config import init_config
from pyemailassistant.logger import init_logger

config = init_config()
logger = init_logger(config["LOGGER"])

def start():
    pass

if __name__ == "__main__":
    start()
