import logging
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ddb_ops():
    def __init__(self):
        logger.info('Calling the domain class')
    
    def put_data():
        # api calls to get data from gaming hub
        player_data = requests.get('https://gaming.uefa.com/en/uclfantasy/services/feeds/players/players_40_en_7.json')
        logger.info(player_data.json())

        # handling dynamodb requests
        
        return player_data