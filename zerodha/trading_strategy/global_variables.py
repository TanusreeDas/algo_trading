import os
import configparser
from zerodha.util import generate_kite as gen_kite, date, logger

# create kite instance for zerodha algo-trading
kite = gen_kite.generate_instance()

# fetch values from config file to initialize trading engine
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, "..", "config", "config_file.ini")
config = configparser.ConfigParser()
config.read(config_file_path)

# Initialize values
log = logger.setup_logger(config.get("trading_setup_attributes", "log_name"))
trading_symbol = logger.setup_logger(
    config.get("trading_setup_attributes", "trading_symbol")
)
no_of_data = int(
    config.get("trading_setup_attributes", "no_of_historical_data_to_fetch")
)
instrument_token = int(config.get("trading_setup_attributes", "instrument_token"))
interval = config.get("trading_setup_attributes", "interval")
continuous = (
    False if config.get("trading_setup_attributes", "continuous") == "False" else True
)
oi = False if config.get("trading_setup_attributes", "oi") == "False" else True
custom_col_1 = config.get("trading_setup_attributes", "cross_over_logic")
trailing_stop_loss = int(config.get("trading_setup_attributes", "stop_loss"))
trailing_profit_target = int(config.get("trading_setup_attributes", "profit_target"))
days_ago = int(config.get("trading_setup_attributes", "days_ago"))
stpt_threshold =int(config.get("trading_setup_attributes","stpt_threshold"))

from_date = date.get_delta_india_time(days_ago)
to_date = date.get_current_india_time()

decision_maker = ""
trade_entry_price = 0
stop_loss_level = 0
target_profit_level = 0

order_id = 555 #need to delete this when we want to place real order
