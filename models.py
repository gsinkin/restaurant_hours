from __future__ import unicode_literals
from datetime import timedelta, datetime
import bisect


def get_delta(open_datetime, close_datetime):
    if close_datetime > open_datetime:
        return close_datetime - open_datetime
    return (close_datetime + timedelta(hours=24)) - open_datetime


class OpenHours(object):

    def __init__(
            self, day_of_week, open_datetime, close_datetime, establishment):
        self.day_of_week = day_of_week
        self.open_datetime = open_datetime
        self.close_delta = get_delta(open_datetime, close_datetime)
        self.establishment = establishment

    def __cmp__(self, other):
        # not checking type
        return cmp(self.open_datetime, other.open_datetime)


class OpenCloseModel(object):

    def __init__(self):
        self.opening_by_day = {
            0: [],  # Sunday
            1: [],  # Monday
            2: [],  # Tuesday
            3: [],  # Wednesday
            4: [],  # Thursday
            5: [],  # Friday
            6: []   # Saturday
        }

    def __getitem__(self, key):
        return self.opening_by_day[key]

    def add(self, open_hours):
        # keep openings sorted by open_time/reverse close_delta on insert
        bisect.insort(self.opening_by_day[open_hours.day_of_week], open_hours)

    def open_establishments(self, check_datetime):
        establishments = []
        # not validating input
        weekday = check_datetime.weekday()
        check_datetime = datetime(
            year=1900, month=1, day=1,
            hour=check_datetime.hour, minute=check_datetime.minute,
            second=check_datetime.second,
            microsecond=check_datetime.microsecond)
        for open_close in self.opening_by_day[weekday]:
            if open_close.open_datetime <= check_datetime:
                if (open_close.open_datetime + open_close.close_delta >
                    check_datetime):
                    establishments.append(open_close.establishment)
            else:
                # we don't have to continue checking times
                break
        return establishments
