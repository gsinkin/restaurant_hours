import time
from parsers import OpenCloseParser


# OpenCloseParser tests
def test_parse_simple():
    parser = OpenCloseParser()
    parser.parse("Test", "Sun 11:30 am - 9 pm")
    open_close = parser.open_close[6]
    sunday_times = open_close[0]
    eleven_thirty = time.strptime("11:30 am", "%I:%M %p")
    nine = time.strptime("9 pm", "%I %p")
    assert sunday_times.open_time == eleven_thirty
    assert sunday_times.close_time == nine
    assert sunday_times.day_of_week == 6
    assert sunday_times.establishment == "Test"


def test_parse_range():
    parser = OpenCloseParser()
    parser.parse("Test1", "Mon-Thu 9 am - 12:20 pm")
    nine = time.strptime("9 am", "%I %p")
    twelve_twenty = time.strptime("12:20 pm", "%I:%M %p")
    for day in xrange(0, 4):
        open_close = parser.open_close[day]
        assert len(open_close) == 1
        times = open_close[0]
        assert times.open_time == nine
        assert times.close_time == twelve_twenty
        assert times.day_of_week == day
        assert times.establishment == "Test1"


def test_parse_day_and_range():
    parser = OpenCloseParser()
    parser.parse("Test2", "Mon-Tue, Thu 9 am - 12:20 pm")
    nine = time.strptime("9 am", "%I %p")
    twelve_twenty = time.strptime("12:20 pm", "%I:%M %p")
    days = [0, 1, 3]
    for day in days:
        open_close = parser.open_close[day]
        assert len(open_close) == 1
        times = open_close[0]
        assert times.open_time == nine
        assert times.close_time == twelve_twenty
        assert times.day_of_week == day
        assert times.establishment == "Test2"


def verify(parser, day, open_time, close_time, establishment):
    open_close = parser.open_close[day]
    found = False
    for times in open_close:
        if (times.open_time == open_time and
            times.close_time == close_time and
            times.day_of_week == day and
            times.establishment == establishment):
            found = True
            break
    if not found:
        raise Exception("Open close time not fund")


def test_parse_multiple_times():
    parser = OpenCloseParser()
    parser.parse("Test3", "Mon 9 am - 12:20 pm / Wed-Thu 12:20 pm - 5 pm")
    nine = time.strptime("9 am", "%I %p")
    twelve_twenty = time.strptime("12:20 pm", "%I:%M %p")
    five = time.strptime("5 pm", "%I %p")
    verify(parser, 0, nine, twelve_twenty, "Test3")
    days = [2, 3]
    for day in days:
        verify(parser, day, twelve_twenty, five, "Test3")


def test_parse_multiple_establishments():
    parser = OpenCloseParser()
    parser.parse("Test4", "Mon 9 am - 12:20 pm")
    parser.parse("TestExtra", "Mon 9 am - 5 pm")
    nine = time.strptime("9 am", "%I %p")
    twelve_twenty = time.strptime("12:20 pm", "%I:%M %p")
    five = time.strptime("5 pm", "%I %p")
    verify(parser, 0, nine, twelve_twenty, "Test4")
    verify(parser, 0, nine, five, "TestExtra")


def test_parse_open_establishments():
    parser = OpenCloseParser()
    parser.parse("Test5", "Mon 9 am - 12:20 pm")
    parser.parse("TestExtra", "Mon 9 am - 5 pm")
    nine = time.strptime("9 am", "%I %p")
    twelve_twenty = time.strptime("12:20 pm", "%I:%M %p")
    one = time.strptime("1 pm", "%I %p")
    five = time.strptime("5 pm", "%I %p")
    verify(parser, 0, nine, twelve_twenty, "Test5")
    verify(parser, 0, nine, five, "TestExtra")
    assert ["Test5", "TestExtra"] == parser.open_close.open_establishments(
        0, twelve_twenty)
    assert ["TestExtra"] == parser.open_close.open_establishments(
        0, one)
    assert [] == parser.open_close.open_establishments(
        1, twelve_twenty)
