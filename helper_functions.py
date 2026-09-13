import os
import datetime
from zoneinfo import ZoneInfo

time_format: str = '%d-%m-%Y %H:%M:%S'


def current_date_time() -> str:
    return datetime.datetime.now(ZoneInfo("Asia/Karachi")).strftime(time_format)


def main_path() -> str:
    return os.getcwd()
