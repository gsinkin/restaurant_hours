import re
from datetime import datetime
from models import OpenCloseModel, OpenHours

DAYS_RE = re.compile("\d+")


class OpenCloseParser(object):

    DAYS = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5,
            "Sun": 6}
    TIME_FORMATS = ("%I:%M %p", "%I %p")

    def __init__(self):
        self.open_close = OpenCloseModel()

    def _extract_days(self, parse_string):
        split = DAYS_RE.split(parse_string)
        if not split:
            return set()
        to_parse = split[0]
        days = set()
        for day_str in to_parse.split(","):
            day_str = day_str.strip()
            day_range = day_str.split("-")
            if len(day_range) == 2:
                # Not validating input str
                opening = self.DAYS[day_range[0]]
                closing = self.DAYS[day_range[1]]
                # Not validating opening < closing
                days.update(set(range(opening, closing + 1)))
            else:
                days.add(self.DAYS[day_str])
        return days

    def _parse_time(self, time_str):
        for time_format in self.TIME_FORMATS:
            try:
                return datetime.strptime(time_str, time_format).time()
            except ValueError:
                pass

    def _extract_hours(self, to_parse):
        match = re.search("\d", to_parse)
        if not match:
            raise ValueError("No open/close time found")
        hours = to_parse[match.start():].split("-")
        # not verifying hours
        opening = hours[0].strip()
        closing = hours[1].strip()
        # not handling bad formatted times
        return (self._parse_time(opening), self._parse_time(closing))

    def parse(self, establishment, parse_string):
        for to_parse in parse_string.split("/"):
            to_parse = to_parse.strip()
            days = self._extract_days(to_parse)
            hours = self._extract_hours(to_parse)
            for day in days:
                open_hours = OpenHours(day, hours[0], hours[1], establishment)
                self.open_close.add(open_hours)
