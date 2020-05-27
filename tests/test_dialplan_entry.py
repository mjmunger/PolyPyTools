import unittest
import os
from unittest_data_provider import data_provider
from poly_py_tools.dialplan_entry import Entry


class TestDialplan(unittest.TestCase):

    def get_column_config(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/csv_columns.map")

    def test_fail_init(self):
        with self.assertRaises(FileNotFoundError):
            entry = Entry("/tmp/3eaaa6ac-fc66-48bd-9874-d0dd491e983f.map")

    def test_init(self):
        entry = Entry(self.get_column_config())
        self.assertEqual(1, entry.map['first'])
        self.assertEqual(0, entry.map['last'])
        self.assertEqual(3, entry.map['exten'])
        self.assertEqual(4, entry.map['vm'])
        self.assertEqual(8, entry.map['mac'])
        self.assertEqual(9, entry.map['email'])
        self.assertEqual(11, entry.map['cid_number'])
        self.assertEqual(7, entry.map['endpoint'])
        self.assertEqual(12, entry.map['label'])
        self.assertEqual(13, entry.map['priority'])
        self.assertEqual(2, entry.map['startrow'])

    provider_test_parse = lambda: (
        (["Viele", "Elliot", "OSnTJuK", "101", "101@testvm", "2025550100", "2125550200", "HahdyMhVj", "0004f23a626f", "eviele@example.org", "atl.example.org", "101", "101", ""], {"last": "Viele", "first": "Elliot", "exten": "101", "vm": "101@testvm", "did": "2025550100", "group_dial": "2125550200", "endpoint": "HahdyMhVj", "mac": "0004f23a626f", "email": "eviele@example.org", "site": "atl.example.org", "cid_number": "101", "label": "101", "priority": ""}),
    )

    @data_provider(provider_test_parse)
    def test_parse(self, row, expected_attribute_values):
        entry = Entry(self.get_column_config())
        entry.parse(row)

        for key in expected_attribute_values:
            self.assertEqual(expected_attribute_values[key], getattr(entry, key), "{} should be {}, got {} instead.".format(key, expected_attribute_values[key], getattr(entry, key)))



