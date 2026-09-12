import datetime
from zoneinfo import ZoneInfo

time_format: str = '%d-%m-%Y %H:%M:%S'
def current_date_time():
    return datetime.datetime.now(ZoneInfo("Asia/Karachi")).strftime(time_format)

#print(type(current_date_time()))