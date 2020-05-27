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

        self.assertEqual(20, len(dialplan.entries))

        with open(self.get_dialplan_csv(), 'r') as dialplan_csv:
            index = 0
            dialplan_csv.__next__()
            reader = csv.reader(dialplan_csv)
            for row in reader:
                index = index + 1
                entry = dialplan.entries.pop(0)
                self.assertEqual(row[0], entry.last, "Failure for entry.{} for index: {}".format("last", index))
                self.assertEqual(row[1], entry.first, "Failure for entry.{} for index: {}".format("first", index))
                self.assertEqual(row[3], entry.exten, "Failure for entry.{} for index: {}".format("exten", index))
                self.assertEqual(row[4], entry.vm, "Failure for entry.{} for index: {}".format("vm", index))
                self.assertEqual(row[5], entry.did, "Failure for entry.{} for index: {}".format("did", index))
                self.assertEqual(row[6], entry.group_dial, "Failure for entry.{} for index: {}".format("group_dial", index))
                self.assertEqual(row[7], entry.endpoint, "Failure for entry.{} for index: {}".format("endpoint", index))
                self.assertEqual(row[8], entry.mac, "Failure for entry.{} for index: {}".format("mac", index))
                self.assertEqual(row[9], entry.email, "Failure for entry.{} for index: {}".format("email", index))
                self.assertEqual(row[10], entry.site, "Failure for entry.{} for index: {}".format("site", index))
                self.assertEqual(row[11], entry.cid_number, "Failure for entry.{} for index: {}".format("cid_number", index))
                self.assertEqual(row[12], entry.label, "Failure for entry.{} for index: {}".format("label", index))
                self.assertEqual(row[13], entry.priority, "Failure for entry.{} for index: {}".format("priority", index))


if __name__ == '__main__':
    unittest.main()
