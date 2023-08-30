import pandas as pd
from datetime import datetime
from zerodha.util import generate_file as create_file, generate_kite as gen_kite

kite = gen_kite.generate_instance()

historical_data = kite.historical_data(
    256265,
    datetime.strptime("2023-08-10", "%Y-%m-%d"),
    datetime.strptime("2023-08-24", "%Y-%m-%d"),
    "5minute",
    continuous=False,
    oi=False,
)

create_file.generate_csv_file("NSE_history_list", pd.DataFrame(historical_data))
create_file.generate_csv_file("NIFTY50_ltp", pd.DataFrame(kite.ltp("NSE:NIFTY 50")))
create_file.generate_csv_file(
    "Instrument", pd.DataFrame(kite.instruments(exchange="NSE"))
)
create_file.generate_csv_file("Order_list", pd.DataFrame(kite.orders()))

# place an order
"""order_id = kite.place_order(variety=kite.VARIETY_REGULAR,
                            tradingsymbol="INFY",
                            exchange=kite.EXCHANGE_NSE,
                            transaction_type=kite.TRANSACTION_TYPE_BUY,
                            quantity=1,
                            order_type=kite.ORDER_TYPE_MARKET,
                            product=kite.PRODUCT_CNC,
                            validity=kite.VALIDITY_DAY)"""
