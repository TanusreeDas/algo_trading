import time
import pandas as pd
import crossover_detection
import order_placement
import risk_management
import eod_tasks
import global_variables
from zerodha.util import date

kite = global_variables.kite
log = global_variables.log


def find_latest_data():
    current_india_time = date.get_current_india_time()

    historical_data = kite.historical_data(
        global_variables.instrument_token,
        global_variables.from_date,
        current_india_time,
        global_variables.interval,
        global_variables.continuous,
        global_variables.oi,
    )
    current_data = kite.ltp("NSE:NIFTY 50")["NSE:NIFTY 50"]["last_price"]

    latest_data = [
        (dict1["date"], dict1["close"])
        for dict1 in historical_data[-global_variables.no_of_data :]
    ]
    latest_data.append((current_india_time, current_data))
    latest_data_df = pd.DataFrame(latest_data, columns=["date", "close"])

    return latest_data_df


def execute_trading_strategy():
    try:
        latest_ltp_data = find_latest_data()
        dates, closing_prices = latest_ltp_data["date"], latest_ltp_data["close"]
        crossovers = crossover_detection.find_crossovers(
            dates.astype(str), closing_prices
        )
        len_crossover = len(crossovers)

        if len_crossover == 1:
            crossover = crossovers[0]
            log.info(f"Only one crossover found. Crossover= {crossover}")
            crossover_detection.send_crossover_email(crossover)

            order_placement.place_order(crossover)

        elif len_crossover > 1:
            log.error(f"more than one crossover found-> {crossovers}")
            crossover_detection.send_multi_crossover_email(crossovers)

        else:
            log.debug("No crossover found.")

        if (
            global_variables.decision_maker != ""
            and not global_variables.cross_over_order_placed
        ):
            latest_closing_price = closing_prices.iloc[-1]
            risk_management.check_profit_margin_and_stop_loss(latest_closing_price)
            log.debug("Stop loss and Profit Target checks are done.")
        global_variables.cross_over_order_placed = False

    except Exception as e:
        log.exception("An error occurred: %s", e)
        log.error(f"This is a generic Exception block")
    except KeyboardInterrupt as e:
        log.exception("User Forcefully stopped execution: %s", e)
        log.error(f"Forcefully program is closed")


def main(caller_desc):
    log.debug(f"Running as a {caller_desc} program.")
    while True:
        current_time = date.get_current_india_time()
        market_closing_time = current_time.replace(
            hour=15, minute=30, second=0, microsecond=0
        )
        time_difference = market_closing_time - current_time
        if time_difference.total_seconds() <= 600:
            eod_tasks.close_all_trades()
            break

        execute_trading_strategy()
        log.warning("Now Program will take 5 minutes Pause..")
        time.sleep(5 * 60)


if __name__ == "__main__":
    main("Standalone")
