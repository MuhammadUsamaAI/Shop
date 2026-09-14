import os
import datetime
from zoneinfo import ZoneInfo
from os import PathLike
time_format: str = '%d-%m-%Y %H:%M:%S'


def current_date_time() -> str:
    return datetime.datetime.now(ZoneInfo("Asia/Karachi")).strftime(time_format)


def main_path() -> str:
    return os.getcwd()


def path_corretor(
    key_to_remove: str, path: str | PathLike[str], key_to_add: str
) -> str:
    path_str = str(path)
    if key_to_remove in path_str:
        path_str = path_str.replace(
            "finance", ""
        )
    return os.path.join(path_str, key_to_add)