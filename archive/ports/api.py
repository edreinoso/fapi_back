import json
import logging
import sys
sys.path.append("./domains")
from put_data import ddb_ops

class player_interface():
    def __init__(self):
        logger.info('Calling the port class')

    def call_domain():
        # initialize the domain
        ddb = ddb_ops

        # handling put operations
        res_domain = ddb.put_data()
        
        return res_domain