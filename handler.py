import json
import request
import put_player_data
## service main responsibility
# 1. get data from gaming hub endpoint
# 2. put data into database

def player_data(event, context):
    # call the adapter
    # adapter calls the port
    # port then calls domain
    # domain interacts with DDB
    


    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
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
