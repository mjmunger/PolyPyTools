class ColumnMapper:

    column_list = None
    config = None

    def __init__(self, config):
        self.config = config
        self.column_list = []

        for item in config.config['dictionary']:
            self.column_list.append(item)


    def match_columns(self, row):
        for column in row:

