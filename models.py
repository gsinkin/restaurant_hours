from __future__ import unicode_literals

import bisect


class OpenHours(object):

    def __init__(self, day_of_week, open_time, close_time, establishment):
        self.day_of_week = day_of_week
        self.open_time = open_time
        self.close_time = close_time
        self.establishment = establishment

    def __cmp__(self, other):
        # not checking type
        result = cmp(self.open_time, other.open_time)
        # sort by open_time/close_time
        return (result if result else cmp(self.close_time, other.close_time))


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
        # keep openings sorted by open_time on insert
        bisect.insort(self.opening_by_day[open_hours.day_of_week], open_hours)

    def open_establishments(self, day_of_week, check_time):
        establishments = []
        # not validating input
        for open_close in self.opening_by_day[day_of_week]:
            if (open_close.open_time <= check_time and
                open_close.close_time > check_time):
                establishments.append(open_close.establishment)
        return establishments
