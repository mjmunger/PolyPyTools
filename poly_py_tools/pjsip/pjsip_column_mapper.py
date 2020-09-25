from poly_py_tools.column_mapper import ColumnMapper
import csv
import json


class PjSipColumnMapper:
    # TODO: This class needs tests!
    container = None
    source_csv = None
    config = None
    pconf = None

    def __init__(self, container):

        self.container = container
        self.args = container['args']

        if 'pconf' in container:
            self.pconf = container['pconf']

    def map_columns(self, source_file):
        with open(source_file) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=",", quotechar='"')
            column_headers = next(csv_reader)

        mapper = ColumnMapper(self.config)
        mapper.match_columns(column_headers)
        self.pconf.json['csvmap'] = mapper.map

        buffer = json.dumps(self.config.json)

        fp = open('polypy.conf', 'w')
        fp.write(buffer)
        fp.close()

    def run(self):
        self.map_columns(self.args['<file>'])
