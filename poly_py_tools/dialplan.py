import os
import csv
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.polypy_config import PolypyConfig


class Dialplan:
    config = None
    csv_path = None
    column_config = None
    entries = None

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.entries = []

    def with_config(self, config: PolypyConfig):

        if not isinstance(config, PolypyConfig):
            raise TypeError("You must pass an object of type PolypyConfig to the Dialplan object.")

        self.config = config
        self.column_config = config.json['csvmap']

    def parse(self):
        if self.column_config is None:
            raise Exception("Cannot parse a dial plan without a column map. Need to use .with_config(column_map) in your code.")
        with open(self.csv_path, 'r') as dialplan_csv:
            # Strip the header
            dialplan_csv.__next__()
            reader = csv.reader(dialplan_csv)
            for row in reader:
                dialplan_entry = Entry(self.config)
                dialplan_entry.parse(row)
                self.entries.append(dialplan_entry)
