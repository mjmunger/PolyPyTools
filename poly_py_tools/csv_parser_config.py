import json
from pprint import pprint


class CSVParserConfig:

    first_name_column = None
    last_name_column = None
    extension_column = None
    voicemail_column = None
    mac_column = None
    email_column = None
    device_column = None
    cid_number = None
    startrow = 0
    site = None
    verbosity = 0

    def __init__(self):
        pass

    def import_column_defs(self, defs):
        for col_def in defs:
            self.transmute(col_def)

    def transmute(self, col_def):
        if not "=" in col_def:
            raise ValueError("column definitions must take the form of column=value")

        if col_def is None:
            raise ValueError("All columns must be supplied for the parser. See polypy sip configure --help")

        buff = col_def.split("=")
        column = buff[0]
        definition = buff[1]

        if not definition.isdigit():
            ascii_value = ord(str(definition).upper())
            definition = ascii_value - 65

        if column == "first":
            self.first_name_column = definition if definition is not None and self.first_name_column is None else "undefined"

        if column == "last":
            self.last_name_column = definition if definition is not None and self.last_name_column is None else "undefined"

        if column == "exten":
            self.extension_column = definition if definition is not None and self.extension_column is None else "undefined"

        if column == "vm":
            self.voicemail_column = definition if definition is not None and self.voicemail_column is None else "undefined"

        if column == "mac":
            self.mac_column = definition if definition is not None and self.mac_column is None else "undefined"

        if column == "email":
            self.email_column = definition if definition is not None and self.email_column is None else "undefined"

        if column == "startrow":
            self.startrow =  definition if definition is not None and self.startrow == 0 else 0

        if column == "cid_number":
            self.cid_number = definition if definition is not None and self.cid_number is None else "undefined"

        if column == "device":
            self.device_column = definition if definition is not None and self.device_column is None else "undefined"

    def set_verbosity(self, verbosity):
        self.verbosity = verbosity

    def save(self):
        settings = {}
        settings['first'] = self.first_name_column
        settings['last'] = self.last_name_column
        settings['exten'] = self.extension_column
        settings['vm'] = self.voicemail_column
        settings['mac'] = self.mac_column
        settings['email'] = self.email_column
        settings['startrow'] = self.startrow
        settings['cid_number'] = self.cid_number
        settings['device'] = self.device_column

        buffer = json.JSONEncoder().encode(settings)
        f = open('csv_columns.map', 'w')
        f.write(buffer)
        f.close()
        print("Settings saved in csv_columns.map")

    def set_site(self, site):
        self.site = site

    def load(self, csv_config_path):
        f = open(csv_config_path,'r')
        buffer = json.load(f)

        self.first_name_column = buffer['first']
        self.last_name_column = buffer['last']
        self.extension_column = buffer['exten']
        self.voicemail_column = buffer['vm']
        self.mac_column = buffer['mac']
        self.email_column = buffer['email']
        self.cid_number = buffer['cid_number']
        self.device_column = buffer['device']
        self.startrow = buffer['startrow']

    def __str__(self):
        buffer = []
        buffer.append("first_name_column: %s" % self.first_name_column)
        buffer.append("last_name_column: %s" % self.last_name_column)
        buffer.append("extension_column: %s" % self.extension_column)
        buffer.append("voicemail_column: %s" % self.voicemail_column)
        buffer.append("mac_column: %s" % self.mac_column)
        buffer.append("email_column: %s" % self.email_column)
        buffer.append("cid_number: %s" % self.cid_number)
        buffer.append("device_column: %s" % self.device_column)
        buffer.append("startrow: %s" % self.startrow)
        return "\n".join(buffer)