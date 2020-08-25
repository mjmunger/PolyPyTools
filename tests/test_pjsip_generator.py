import json
import os
import unittest
from unittest import mock
from unittest.mock import patch, mock_open, MagicMock
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.pjsip_generator import PJSipGenerator
from poly_py_tools.polypy_config import PolypyConfig
from pwgen_secure.rpg import Rpg


class TestPJSipGenerator(unittest.TestCase):

    def base_config(self):
        return {"lib_path":"/var/lib/polypy","share_path":"/usr/share/polypy/","config_path":"","package_path":"/usr/local/lib/python3.7/dist-packages/poly_py_tools","server_addr":"pbx.example.org","paths":{"asterisk":"","tftproot":""}}

    def test_use(self):
        config = "asdfasdf"
        generator = PJSipGenerator()
        generator.use(config)
        self.assertEqual(config, generator.config)

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
        ( 'DialPlanBuilder-ExampleOrg.csv', 'expected_pjsip_01.conf'),
    )

    @data_provider(provider_test_generator)
    def test_generate(self, csv, expected_conf):
        mock_rpg = Rpg("strong", None)
        mock_rpg.generate_password = MagicMock(return_value="QoWTIllrgkVKZR")

        config = self.base_config()
        config['paths']['asterisk'] = '/tmp/'
        csv_path = os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator/{}".format(csv))
        expected_conf_path = os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator/{}".format(expected_conf))

        config = PolypyConfig()
        config.add_search_path(os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator/"))
        config.load()

        f = open(expected_conf_path, 'r')
        buffer = f.read()
        f.close()
        expected_configs = "".join(buffer)

        generator = PJSipGenerator()
        # self.assertRaises(ValueError, generator.generate_from(csv_path))
        generator.use(config)
        generator.with_rpg(mock_rpg)
        generator.generate_from(csv_path)
        self.assertEqual(expected_configs, generator.conf())


if __name__ == '__main__':
    unittest.main()
