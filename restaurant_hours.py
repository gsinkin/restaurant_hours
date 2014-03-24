import csv

from parsers import OpenCloseParser


def find_open_restaurants(csv_filename, search_datetime):
    parser = OpenCloseParser()
    with open(csv_filename, "r") as infile:
        reader = csv.reader(infile)
        for row in reader:
            parser.parse(row[0], row[1])
    return parser.open_close.open_establishments(search_datetime)
