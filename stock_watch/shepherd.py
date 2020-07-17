import configparser
import alpaca_trade_api as tradeapi

config = configparser.ConfigParser()
config.read('../config.ini')

api_key = config['ALPACA']['api_key']
secret_key = config['ALPACA']['secret_key']

api = tradeapi.REST(key_id=api_key,
                    secret_key=secret_key,
                    base_url="https://paper-api.alpaca.markets",
                    api_version='v2')

account = api.get_account()










