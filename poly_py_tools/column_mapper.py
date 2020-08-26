class ColumnMapper:

    column_list = None
    config = None
    map = None

    def __init__(self, config):
        self.config = config
        self.column_list = []

        for item in config.json['dictionary']:
            self.column_list.append(item)


    def match_columns(self, row):
        map = {}
        for word in self.config.json['dictionary']:
            map[word] = None

        column_counter = -1
        for header in row:
            header = header.lower().strip()
            column_counter = column_counter + 1
            for word in self.config.json['dictionary']:
                if str(header) in list(self.config.json['dictionary'][word]):
                    map[word] = column_counter
                    break
        self.map = map
        return self.map
