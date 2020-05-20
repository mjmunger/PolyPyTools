import unittest
import os
import csv
from unittest_data_provider import data_provider
from poly_py_tools.dialplan import Dialplan


class TestDialplan(unittest.TestCase):

    def get_dialplan_csv(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/dialplanbuilder_sample.csv")

    def get_column_config(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/csv_columns.map")

    def test_init(self):
        dialplan = Dialplan(self.get_dialplan_csv())
        self.assertEqual(self.get_dialplan_csv(), dialplan.csv_path)

    def test_fail_with_config(self):
        dialplan = Dialplan(self.get_dialplan_csv())
        with self.assertRaises(FileNotFoundError):
            dialplan.with_config("/tmp/9c152c3f-b020-45c6-a6d8-de67dd16b0b1.map")

    def test_with_config(self):
        dialplan = Dialplan(self.get_dialplan_csv())
        dialplan.with_config(self.get_column_config())
        self.assertEqual(dialplan.column_config, self.get_column_config())

    def test_parse(self):
        dialplan = Dialplan(self.get_dialplan_csv())
        dialplan.with_config(self.get_column_config())
        dialplan.parse()

        self.assertEqual(20, dialplan.rows)

if __name__ == '__main__':
    unittest.main()
