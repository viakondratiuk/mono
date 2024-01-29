from datetime import datetime


def get_end_of_day(date_obj: datetime) -> datetime:
    return date_obj.replace(hour=23, minute=59, second=59)


def get_timestamp(date_obj: datetime, end_of_day: bool = False) -> int:
    if end_of_day:
        date_obj = get_end_of_day(date_obj)
    return int(date_obj.timestamp())
