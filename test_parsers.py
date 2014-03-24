from datetime import datetime, timedelta
from parsers import OpenCloseParser


def verify(parser, day, open_datetime, close_delta, establishment):
    open_close = parser.open_close[day]
    found = False
    for times in open_close:
        if (times.open_datetime == open_datetime and
            times.close_delta == close_delta and
            times.day_of_week == day and
            times.establishment == establishment):
            found = True
            break
    if not found:
        raise Exception("Open close time not fund")


# OpenCloseParser tests
def test_parse_simple():
    parser = OpenCloseParser()
    parser.parse("Test", "Sun 11:30 am - 9 pm")
    eleven_thirty = datetime.strptime("11:30 am", "%I:%M %p")
    nine = datetime.strptime("9 pm", "%I %p")
    verify(parser, 6, eleven_thirty, nine - eleven_thirty, "Test")


def test_parse_range():
    parser = OpenCloseParser()
    parser.parse("Test1", "Mon-Thu 9 am - 12:20 pm")
    nine = datetime.strptime("9 am", "%I %p")
    twelve_twenty = datetime.strptime("12:20 pm", "%I:%M %p")
    for day in xrange(0, 4):
        verify(parser, day, nine, twelve_twenty - nine, "Test1")


def test_parse_day_and_range():
    parser = OpenCloseParser()
    parser.parse("Test2", "Mon-Tue, Thu 9 am - 12:20 pm")
    nine = datetime.strptime("9 am", "%I %p")
    twelve_twenty = datetime.strptime("12:20 pm", "%I:%M %p")
    days = [0, 1, 3]
    for day in days:
        verify(parser, day, nine, twelve_twenty - nine, "Test2")


def test_parse_multiple_times():
    parser = OpenCloseParser()
    parser.parse("Test3", "Mon 9 am - 12:20 pm / Wed-Thu 12:20 pm - 5 pm")
    nine = datetime.strptime("9 am", "%I %p")
    twelve_twenty = datetime.strptime("12:20 pm", "%I:%M %p")
    five = datetime.strptime("5 pm", "%I %p")
    verify(parser, 0, nine, twelve_twenty - nine, "Test3")
    days = [2, 3]
    for day in days:
        verify(parser, day, twelve_twenty, five - twelve_twenty,
               "Test3")


def test_parse_multiple_establishments():
    parser = OpenCloseParser()
    parser.parse("Test4", "Mon 9 am - 12:20 pm")
    parser.parse("TestExtra", "Mon 9 am - 5 pm")
    nine = datetime.strptime("9 am", "%I %p")
    twelve_twenty = datetime.strptime("12:20 pm", "%I:%M %p")
    five = datetime.strptime("5 pm", "%I %p")
    verify(parser, 0, nine, twelve_twenty - nine, "Test4")
    verify(parser, 0, nine, five - nine, "TestExtra")


def test_parse_overflow():
    parser = OpenCloseParser()
    parser.parse("Test3", "Mon 9 am - 12 am")
    nine = datetime.strptime("9 am", "%I %p")
    twelve_am = datetime.strptime("12 am", "%I %p")
    verify(parser, 0, nine, twelve_am + timedelta(hours=24) - nine,
           "Test3")


def test_parse_open_establishments():
    parser = OpenCloseParser()
    parser.parse("Test5", "Mon 9 am - 12:20 pm")
    parser.parse("TestExtra", "Mon 9 am - 5 pm")
    parser.parse("TestOverflow", "Mon 4:30 pm - 5 am")
    nine = datetime.strptime("9 am", "%I %p")
    twelve_twenty = datetime.strptime("12:20 pm", "%I:%M %p")
    one = datetime.strptime("1 pm", "%I %p")
    five = datetime.strptime("5 pm", "%I %p")
    verify(parser, 0, nine, twelve_twenty - nine, "Test5")
    verify(parser, 0, nine, five - nine, "TestExtra")
    assert ["Test5", "TestExtra"] == parser.open_close.open_establishments(
        twelve_twenty - timedelta(minutes=20))
    assert ["TestExtra"] == parser.open_close.open_establishments(
        one)
    assert ["TestExtra", "TestOverflow"] == parser.open_close.open_establishments(
        five - timedelta(minutes=20))
    assert ["TestOverflow"] == parser.open_close.open_establishments(
        twelve_twenty + timedelta(hours=6))
    assert ["TestOverflow"] == parser.open_close.open_establishments(
        one + timedelta(hours=12))
    assert [] == parser.open_close.open_establishments(
        twelve_twenty + timedelta(hours=24))
