import schedule
import time
from ..trading_strategy import find_crossover as fc

def run_program():
    # Your code here
    fc.main()

# Schedule the program to run every 1 minute
schedule.every(1).minutes.do(run_program)

while True:
    schedule.run_pending()
    time.sleep(1)
