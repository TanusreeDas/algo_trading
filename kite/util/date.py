from datetime import datetime
from dateutil import parser
import pytz

def get_current_india_time():
    # Get the current Indiatime
    current_time_utc = datetime.now(pytz.utc)
    india_time_zone = pytz.timezone('Asia/Kolkata')
    current_india_time = current_time_utc.astimezone(india_time_zone)
    india_time_string = current_india_time.strftime \
        ('%Y-%m-%d %H:%M:%S %z')  # to keep the date format same as kite history data
    parsed_india_time = parser.parse(india_time_string)

    return parsed_india_time