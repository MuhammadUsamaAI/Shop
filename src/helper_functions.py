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
    path: str | PathLike[str],
    key_to_remove: str | None = None,
    key_to_add: str | None = None,
) -> str:
  path_str = str(path)

  if key_to_remove:
    # Normalize removes trailing slashes so os.path.split isolates the true last folder
    path_str = os.path.normpath(path_str)
    head, tail = os.path.split(path_str)

    if tail == key_to_remove:
      path_str = head
    else:
      raise ValueError(f"Path does not end with '{key_to_remove}'")

  if key_to_add:
    path_str = os.path.join(path_str, key_to_add)

  return path_str