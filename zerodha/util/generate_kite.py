import os
import configparser
from kiteconnect import KiteConnect


def generate_instance():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(current_dir, "..", "config", "config_file.ini")
    config = configparser.ConfigParser()

    # Read and Access configuration values
    config.read(config_file_path)
    api_key = config.get("login_details", "api_key")
    access_token = config.get("login_details", "access_token")

    kite = KiteConnect(api_key)
    kite.set_access_token(access_token)

    return kite
