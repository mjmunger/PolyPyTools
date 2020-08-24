import json
import os
import unittest
from unittest import mock
from unittest.mock import patch
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.PJSipGenerator import PJSipGenerator


class TestPJSipGenerator(unittest.TestCase):

    @mock.patch("os.path")
    def test_generate_from_file_exists(self, mock_path):

        generator = PJSipGenerator()
        existing_file = "/this/file/exists"

        mock_path.exists = lambda path : True
        generator.generate_from(existing_file)
        self.assertEqual(existing_file, generator.source_csv)

    @mock.patch("os.path")
    def test_generate_from_file_not_exists(self, mock_path):
        non_existant_file = "/this/file/does/not/exist"
        generator = PJSipGenerator()

        mock_path.exists = lambda path: False
        with self.assertRaises(FileNotFoundError):
            generator.generate_from(non_existant_file)

    provider_test_generator = lambda : (
        ( 'csv1.csv', 'expected_pjsip_01.conf'),
    )

    def test_use(self):
        config = "asdfasdf"
        generator = PJSipGenerator()
        generator.use(config)
        self.assertEqual(config, generator.config)

    @data_provider(provider_test_generator)
    def test_generate(self, csv, expected_conf):
        base_config_path = os.path.join(os.path.dirname(__file__), 'fixtures/base_config.json')

        fp = open(base_config_path, 'r')
        config = json.load(fp)
        fp.close()

        config['paths']['asterisk'] = '/tmp/'

        generator = PJSipGenerator()
        generator.use(config)
        generator.generate_from(csv)
        self.assertEqual(expected_conf, generator.conf())


if __name__ == '__main__':
    unittest.main()
