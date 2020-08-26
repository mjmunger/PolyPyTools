import os
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.polypy_config import PolypyConfig


class Payload:

    dialplan_entry = None
    provisioned_directory = None
    config = None
    sources = None

    def __init__(self, config:PolypyConfig, dialplan_entry: Entry):

        self.dialplan_entry = dialplan_entry
        self.config = config

        buffer = str(self.dialplan_entry.site).split(".")
        buffer.reverse()
        self.provisioned_directory = ".".join(list(buffer))

        self.sources = []
        self.build_sources()

    def build_sources(self):
        self.sources.append(os.path.join(str(self.config.json['paths']['tftproot']), self.dialplan_entry.mac))
        self.sources.append(os.path.join(str(self.config.json['paths']['tftproot']), self.dialplan_entry.mac + ".cfg"))
        self.sources.append(os.path.join(str(self.config.json['paths']['tftproot']), self.dialplan_entry.mac + "-directory.xml"))

    def __str__(self):
        buffer = []
        for attr, value in self.__dict__.items():
            buffer.append("{}: {}".format(attr,value))
        return "\n".join(buffer)
