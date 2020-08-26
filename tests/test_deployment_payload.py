import unittest
import os
import json

from tempfile import NamedTemporaryFile
from unittest_data_provider import data_provider
from unittest.mock import Mock, MagicMock
from poly_py_tools.payload import Payload
from poly_py_tools.dialplan_entry import Entry
from poly_py_tools.polypy_config import PolypyConfig


class TestPayload(unittest.TestCase):

    def get_column_map(self):
        with open(os.path.join(os.path.dirname(__file__), "fixtures/csv_columns.map"), 'r') as fp:
            return json.load(fp)

    provider_test_init = lambda : (
        # customer               expected_directory
        ("masseyautomotive.com", "com-masseyautomotive"),
    )

    provider_test_payload = lambda : (
            (["Viele", "Elliot", "OSnTJuK", "101", "101@testvm", "2025550100", "2125550200", "HahdyMhVj", "0004f23a626f", "eviele@example.org", "atl.example.org", "101", "101",""]),
        )

    provider_dialplan_rows = lambda : (
            (["Viele", "Elliot", "OSnTJuK", "101", "101@testvm", "2025550100", "2125550200", "HahdyMhVj", "0004f23a626f", "eviele@example.org", "atl.example.org", "101", "101",""], "org.example.atl"),
        )

    @data_provider(provider_dialplan_rows)
    def test_init(self, row, expected_directory):
        with NamedTemporaryFile() as f:
            configs = PolypyConfig()
            configs.set_default_config(f.name)
            configs.json = {}
            configs.json['paths'] = {}
            configs.json['csvmap'] = self.get_column_map()
            configs.json['paths']['asterisk'] = "/etc/asterisk/"
            configs.json['paths']['tftproot'] = "/srv/tftp/"

            entry = Entry(configs)
            entry.parse(row)

            payload = Payload(configs, entry)
            self.assertEqual(entry, payload.dialplan_entry)
            self.assertEqual(expected_directory, payload.provisioned_directory)

            self.assertTrue(isinstance(payload.config, PolypyConfig))
            self.assertTrue(isinstance(payload.dialplan_entry, Entry))

    @data_provider(provider_dialplan_rows)
    def test_rsync_filelist_entry(self, row, expected_directory):
        with NamedTemporaryFile() as f:
            configs = PolypyConfig()
            configs.set_default_config(f.name)
            configs.json['csvmap'] = self.get_column_map()
            configs.json['paths']['asterisk'] = "/etc/asterisk/"
            configs.json['paths']['tftproot'] = "/srv/tftp/"

            entry = Entry(configs)
            entry.parse(row)

            payload = Payload(configs, entry)
            sources = []
            sources.append(os.path.join("/srv/tftp", entry.mac))
            sources.append(os.path.join("/srv/tftp", entry.mac + ".cfg"))
            sources.append(os.path.join("/srv/tftp", entry.mac + "-directory.xml"))

            self.assertEqual(len(sources), len(payload.sources))
            i = 0
            for source in sources:
                self.assertEqual(source, sources[i])
                i = i + 1


if __name__ == '__main__':
    unittest.main()
