import os
import csv
import unittest
from unittest.mock import Mock, MagicMock
from tempfile import TemporaryDirectory, NamedTemporaryFile
from unittest_data_provider import data_provider
from poly_py_tools.directory_item import DirectoryItem
from poly_py_tools.directory import Directory
from poly_py_tools.polypy_config import PolypyConfig


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
        directory.add_csv(test_csv)
        directory.read()
        self.assertEqual(expected_directory_body, directory.render())

    def test_csv_not_exist(self):

        directory = Directory("bac58fc0b629")
        with self.assertRaises(FileNotFoundError):
            directory.add_csv("/tmp/8f2b6a37-a96e-4d79-be48-2349b769d897.csv")
            directory.read()

    provider_test_read = lambda : (
        #Mac address Files                                                                  Expected item count
        ("AC:47:4A:96:B0:41", ("speed-dial-test.csv",),                                                7),
        ("D2:E5:3B:FB:03:BA", ("speed-dial-test.csv", "speed-dial-test2.csv"),                         18),
        ("5F:61:82:4A:26:39", ("speed-dial-test.csv", "speed-dial-test2.csv", "user-bw-test.csv"),     24),
    )

    @data_provider(provider_test_read)
    def test_add_csv(self, mac_address, files, expected_item_count):
        fixtures_root = os.path.join(os.path.dirname(__file__), "fixtures")
        directory = Directory(mac_address)

        for file in files:
            directory.add_csv(os.path.join(fixtures_root, file))

        self.assertEqual(len(files), len(directory.csv_files))

    @data_provider(provider_test_read)
    def test_read(self, mac_address, files, expected_item_count):
        file = None
        fixtures_root = os.path.join(os.path.dirname(__file__), "fixtures")

        directory = Directory(mac_address)
        for file in files:
            test_csv = os.path.join(fixtures_root, file)
            directory.add_csv(test_csv)

        directory.read()

        self.assertEqual(expected_item_count, len(directory.items))

        counter = -1

        for file in files:
            target_csv = os.path.join(fixtures_root, file)
            # print("Processing: {}".format(target_csv))

            with open(target_csv, 'r') as csvfile:
                # Skip the header
                csvfile.__next__()
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    row = [col.strip() for col in row]
                    counter = counter + 1
                    # print("Counter: {}".format(counter))
                    target_item = None
                    target_item = directory.items[counter]

                    self.assertEqual(row[0], target_item.first_name)
                    self.assertEqual(row[1], target_item.last_name)
                    self.assertEqual(row[2], target_item.contact)
                    self.assertEqual("Yes" if row[3] == "Yes" else "No", "Yes" if target_item.buddy_watch == 1 else "No")
                    self.assertEqual(row[4], target_item.label)

            header_exists = False
            for item in directory.items:
                if item.first_name == "First" and item.last_name == "Last" and item.contact == "Number":
                    header_exists = True
            self.assertFalse(header_exists)

    provider_test_multiple_csvs_output = lambda : (
        ("5F:61:82:4A:26:39", ("file1.csv", "file2.csv", "file3.csv"), "expected_directory.xml", 32),
    )

    @data_provider(provider_test_multiple_csvs_output)
    def test_multiple_csvs(self, mac_address, files, expected_directory, expected_item_count):
        fixtures_root = os.path.join(os.path.dirname(__file__), "fixtures")

        with open(os.path.join(fixtures_root, "csvfiles/{}".format(expected_directory)), 'r') as fp:
            expected_directory_xml = fp.read()

        directory = Directory(mac_address)
        for csv in files:
            directory.add_csv(os.path.join(fixtures_root, "csvfiles/{}".format(csv)))

        directory.read()
        self.assertEqual(expected_item_count, len(directory.items))

        with TemporaryDirectory() as tmpdir:
            with NamedTemporaryFile() as f:
                configs = PolypyConfig()
                configs.set_default_config(f.name)
                configs.json['paths']['tftproot'] = str(tmpdir)

                directory.save(configs.json)

                with open(os.path.join(tmpdir, mac_address.replace(":", "").replace("-", "").lower().strip() + "-directory.xml"), 'r') as actual_directory_xml:
                    self.assertEqual(expected_directory_xml, actual_directory_xml.read())


if __name__ == '__main__':
    unittest.main()
