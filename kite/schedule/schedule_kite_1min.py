import schedule
import time
from kite.trading_strategy import find_crossover as fc


def schedule_job():
    schedule.every(1).minutes.do(fc.main())


while True:
    schedule.run_pending()
    time.sleep(1)
