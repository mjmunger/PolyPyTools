import os
import csv


class Dialplan:
    csv_path = None
    column_config = None

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def with_config(self, column_map):
        if not os.path.exists(column_map):
            raise FileNotFoundError

        self.column_config = column_map

    def parse(self):
        with open(self.csv_path, 'r') as dialplan_csv:
            reader = csv.reader(dialplan_csv)
            for row in reader:
                dialplan_entry = Entry(self.column_config)
                dialplan_entry.parse(row)
                self.entries.append(dialplan_entry)
