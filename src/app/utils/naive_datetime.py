import datetime
from typing import Any


def make_datetime_naive(dt: Any) -> Any:
    if isinstance(dt, datetime.datetime) and dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


def clean_model_datetimes(obj: Any, fields: list[str]):
    for field in fields:
        value = getattr(obj, field, None)
        if value is not None:
            setattr(obj, field, make_datetime_naive(value))
