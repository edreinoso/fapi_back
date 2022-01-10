import sys
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
    res = adapter.invoke_port_interface()

    return res

    # port then calls domain
    # domain interacts with DDB
