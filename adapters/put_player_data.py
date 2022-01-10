import json
import logging
import sys
sys.path.append("./ports")
from api import player_interface

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class player_adapter():
    
    def __init__(self):
        logger.info('Calling the adapter class')

    def invoke_port_interface():
        # initializing the port
        port = player_interface

        # creating the http request
        res_port = player_interface.call_domain()

        body = {
            "message": "UCL Serverless v1.3: hexagonal arch structure!",
            "res": res_port
        }

        res = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return body
