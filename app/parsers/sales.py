import csv
from enum import IntEnum

class Fields(IntEnum):
    retailer_country = 0
    order_method_type = 1
    retailer_type = 2
    product_line = 3
    product_type = 4
    product = 5
    year = 6
    quarter = 7
    revenue = 8
    quantity = 9
    gross_margin = 10


class Parser():

    def __init__(self, filename):
        self.filename = filename
        self.fields = []

    def parse_sale(self):
        with open(self.filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            # ignore header row
            next(reader)
            for row in reader:
                # for now skip invalid sales
                if self._valid_sale(row):
                    yield row

    def _valid_sale(self, row):
        # TODO: add real validation and error handling code
        if row[Fields.gross_margin] == "":
            return False
        return True
