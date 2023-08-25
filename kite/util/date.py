from datetime import datetime, timedelta
from dateutil import parser
import pytz


def get_current_india_time():
    # Get the current Indiatime
    current_time_utc = datetime.now(pytz.utc)
    india_time_zone = pytz.timezone("Asia/Kolkata")
    current_india_time = current_time_utc.astimezone(india_time_zone)
    india_time_string = current_india_time.strftime(
        "%Y-%m-%d %H:%M:%S %z"
    )  # to keep the date format same as kite history data
    parsed_india_time = parser.parse(india_time_string)

    return parsed_india_time


def get_delta_india_time(days):
    # Get the current Indiatime
    delta_time_utc = datetime.now(pytz.utc) - timedelta(days)
    india_time_zone = pytz.timezone("Asia/Kolkata")
    delta_india_time = delta_time_utc.astimezone(india_time_zone)
    india_time_string = delta_india_time.strftime(
        "%Y-%m-%d %H:%M:%S %z"
    )  # to keep the date format same as kite history data
    parsed_time = parser.parse(india_time_string)

    return parsed_time
