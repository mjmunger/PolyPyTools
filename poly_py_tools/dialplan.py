import os

class Dialplan:
    csv_path = None
    column_config = None

    def __init__(self, csv_path):
        self.csv_path = csv_path

    def with_config(self, column_map):
        if not os.path.exists(column_map):
            raise FileNotFoundError

        self.column_config = column_map