import pandas as pd
from datetime import datetime
from kite.util import generate_file as create_file, generate_kite as gen_kite

kite = gen_kite.generate_instance()

historical_data=kite.historical_data( 256265, datetime.strptime("2023-08-10", "%Y-%m-%d"), datetime.strptime("2023-08-24", "%Y-%m-%d"), "5minute", continuous=False, oi=False)

create_file.generate_csv_file('NSE_history_list',pd.DataFrame(historical_data))
create_file.generate_csv_file('NIFTY50_ltp',pd.DataFrame(kite.ltp("NSE:NIFTY 50")))
create_file.generate_csv_file('instrument',pd.DataFrame(kite.instruments(exchange='NSE')))