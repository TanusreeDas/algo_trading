import schedule
import time
from zerodha.trading_strategy import algo_trading_engine as fc


def schedule_job():
    schedule.every(1).minutes.do(fc.main())


while True:
    schedule.run_pending()
    time.sleep(1)
