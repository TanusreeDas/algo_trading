from kiteconnect import KiteConnect
import os
import configparser

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, '..', 'config', 'config_file.ini')
config = configparser.ConfigParser()

# Read and Access configuration values
config.read(config_file_path)
api_key = config.get('login_details', 'api_key')
request_token=config.get('login_details', 'request_token')
api_secret=config.get('login_details', 'api_secret')

kite = KiteConnect(api_key=api_key)
data = kite.generate_session(request_token=request_token, api_secret=api_secret)

config.set('login_details', 'access_token',data["access_token"])
print("access token is-> ",data["access_token"]," save this one for future use.")

with open(config_file_path, 'w') as configfile:
    config.write(configfile)