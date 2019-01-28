class CSVParserConfig:

    first_name_column = None
    last_name_column = None
    extension_column = None
    voicemail_column = None
    mac_column = None
    email_column = None
    verbosity = 0

    def __init__(self):
        pass

    def import_column_defs(self, defs):
        self.first_name_column = self.transmute(['first'])
        self.last_name_column = self.transmute(['last'])
        self.extension_column = self.transmute(['exten'])
        self.voicemail_column = self.transmute(['vm'])
        self.mac_column = self.transmute(['mac'])
        self.email_column = self.transmute(['email'])

    def transmute(self, column):
        if column.isdigit():
            return True

        ascii_value = ord(str(column).upper())
        column_value = ascii_value - 65
        return column_value

    def set_verbosity(self, verbosity):
        self.verbosity = verbosity