import os
import csv
import unittest
from unittest_data_provider import data_provider
from poly_py_tools.directory_item import DirectoryItem
from poly_py_tools.directory import Directory


class TestDirectory(unittest.TestCase):

    provider_test_init = lambda : (
        # Mac address         expected_mac
        ("BA:C5:8F:C0:B6:29", "bac58fc0b629"),
        ("ba:c5:8f:c0:b6:29", "bac58fc0b629"),
        ("ba-c5-8f-c0-b6-29", "bac58fc0b629"),
        ("bac58fc0b629", "bac58fc0b629"),
    )

    @data_provider(provider_test_init)
    def test_init(self, mac, expected_mac):

        directory = Directory(mac)
        self.assertEqual(directory.mac_addr, expected_mac)

    def test_generate_directory(self):
        fixtures_root = os.path.join(os.path.dirname(__file__), "fixtures")
        test_csv = os.path.join(fixtures_root, "speed-dial-test.csv")
        expected_directory = os.path.join(fixtures_root, "expected_directory.xml")

        self.assertEqual(True, os.path.exists(test_csv))
        self.assertEqual(True, os.path.exists(expected_directory))

        f = open(expected_directory, 'r')
        expected_directory_body = f.read()
        f.close()

        directory = Directory("bac58fc0b629")
        directory.read(test_csv)
        self.assertEqual(expected_directory_body, directory.render())

    def test_csv_not_exist(self):

        directory = Directory("bac58fc0b629")
        with self.assertRaises(FileNotFoundError):
            directory.read("/tmp/8f2b6a37-a96e-4d79-be48-2349b769d897.csv")

    def test_read(self):
        fixtures_root = os.path.join(os.path.dirname(__file__), "fixtures")
        test_csv = os.path.join(fixtures_root, "speed-dial-test.csv")

        self.assertEqual(True, os.path.exists(test_csv))

        directory = Directory("bac58fc0b629")
        directory.read(test_csv)

        f = open(test_csv, 'r')
        lines = f.readlines()
        f.close()

        self.assertEqual(len(lines) -1, len(directory.items))

        counter = -1
        with open(test_csv, 'r') as csvfile:
            csvfile.__next__() #Skip the header
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                counter = counter + 1

                target_item = directory.items[counter]

                self.assertEqual(row[0], target_item.first_name)
                self.assertEqual(row[1], target_item.last_name)
                self.assertEqual(row[2], target_item.contact)

        with open(test_csv, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            header_row = next(csv_reader)

            header_exists = False
            for item in directory.items:
                if item.first_name == "First" and item.last_name == "Last" and item.contact == "Number":
                    header_exists = True
            self.assertFalse(header_exists)


if __name__ == '__main__':
    unittest.main()
