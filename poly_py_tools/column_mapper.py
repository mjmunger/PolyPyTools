class ColumnMapper:

    column_list = None
    pconf = None
    map = None

    def __init__(self, pconf):
        self.pconf = pconf
        self.column_list = []

        for item in pconf.json['dictionary']:
            self.column_list.append(item)

    def match_columns(self, row):
        map = {}
        for word in self.pconf.json['dictionary']:
            map[word] = None

        column_counter = -1
        for header in row:
            header = header.lower().strip()
            column_counter = column_counter + 1
            for word in self.pconf.json['dictionary']:
                if str(header) in list(self.pconf.json['dictionary'][word]):
                    map[word] = column_counter
                    break
        self.map = map
        return self.map
