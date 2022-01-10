import json
import sys
import requests
sys.path.append("./adapters")
from put_player_data import player_adapter
# import requests
## service main respsls onsibility
# 1. get data from gaming hub endpoint
# 2. put data into database

def player_data(event, context):
    # call the adapter
    adapter = player_adapter

    # adapter calls the port
    adapter.call_port()

    # port then calls domain
    # domain interacts with DDB

    body = {
        "message": "UCL Serverless v1.2: calling classes!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
