import unittest
from unittest_data_provider import data_provider
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory
from poly_py_tools.column_mapper import ColumnMapper
from poly_py_tools.polypy_config import PolypyConfig


class TestColumnMapper(unittest.TestCase):

    def test_init(self):
        expected_column_list = ["first", "last", "exten", "vm", "mac", "email", "device", "cid_number", "priority", "label", "model", "did", "group_dial", "site"]

        with NamedTemporaryFile() as f:
            config = PolypyConfig()
            config.set_default_config(f.name)

            mapper = ColumnMapper(config)

            self.assertEqual(expected_column_list, mapper.column_list)

    provider_column_headers = lambda: (
        (["Last name", "First Name", "Title", "Extension ", "Voicemail ", "Direct Phone", "Simul-ring", "Device", "Model", "MAC", "Email", "site", "callerid", "label", "priority"], {"first": 1, "last": 0, "exten": 3, "vm": 4, "mac": 9, "email": 10, "device": 7, "cid_number": 12, "priority": 14, "label": 13, "model": 8, "did": 5, "group_dial": 6, "site": 11 }),
    )

    @data_provider(provider_column_headers)
    def test_match_columns(self, column_headers, expected_dictionary):
        with NamedTemporaryFile() as f:
            config = PolypyConfig()
            config.set_default_config(f.name)
            mapper = ColumnMapper(config)
            mapper.match_columns(column_headers)
            self.assertEqual(expected_dictionary, mapper.match_columns(column_headers))


if __name__ == '__main__':
    unittest.main()
