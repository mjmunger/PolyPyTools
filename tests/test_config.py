import unittest
import os.path
import json
import copy
from tempfile import NamedTemporaryFile

from unittest_data_provider import data_provider

from poly_py_tools.polypy_config import PolypyConfig
from unittest.mock import patch, mock_open, Mock, MagicMock


class TestConfig(unittest.TestCase):
    provider_test_find_config = lambda: (
        # check_paths                                    expected_config_path
        (["/path/to/current/directory", "/etc/polypy/"], "/path/to/current/directory/polypy.conf", True),
        (["/path/to/current/directory", "/etc/polypy/"], "/etc/polypy/polypy.conf", True),
        (["/path/to/current/directory", "/etc/polypy/"], None, False),
    )

    @data_provider(provider_test_find_config)
    def test_find_config(self, check_paths, expected_config_path, exists):
        os.path.exists = lambda path: path == expected_config_path

        config = PolypyConfig()
        for path in check_paths:
            config.add_search_path(path)

        self.assertEqual(exists, config.find())
        self.assertEqual(expected_config_path, config.config_path)

    @staticmethod
    def create_config_tuples():
        fixtures_dir = os.path.join(os.path.dirname(__file__),'fixtures/')
        base_config_path = os.path.join(fixtures_dir, "base_config.json")

        with open(base_config_path) as fp:
            base_config = json.load(fp)

        return_tuples = ()

        config1 = copy.deepcopy(base_config)
        config1['config_path'] = fixtures_dir
        config1['paths']['asterisk'] = os.path.join(fixtures_dir, "tests/fixtures/etc/asterisk/")
        config1['paths']['tftproot'] = os.path.join(fixtures_dir, "tests/fixtures/srv/tftp/")
        return_tuples = return_tuples + ( (json.dumps(config1),["/path/to/current/directory", "/etc/polypy/"], "/path/to/current/directory/polypy.conf",),)

        return return_tuples

    config_fixtures = lambda : TestConfig.create_config_tuples()

    @data_provider(config_fixtures)
    def test_load_config(self, config, check_paths, expected_config_path):
        os.path.exists = lambda path: path == expected_config_path

        expected_config_object = json.loads(config)

        with patch("builtins.open", mock_open(read_data=config)) as mock_file:
            assert open(expected_config_path).read() == config
            mock_file.assert_called_with(expected_config_path)

            config = PolypyConfig()
            for path in check_paths:
                config.add_search_path(path)
            config.find()
            config.load()
            print(config.config)
            self.assertEqual(expected_config_object, config.config)

    def test_add_search_path(self):
        config = PolypyConfig()
        config.add_search_path("/path/to/some/place")
        config.add_search_path("/etc/polypy")

        self.assertEqual(2,len(config.search_paths))

    @data_provider(config_fixtures)
    def test_write_config(self, config_string, check_paths, expected_config_path):
        config = PolypyConfig()
        config.config = json.loads(config_string)

        f = NamedTemporaryFile(delete=False)
        config.config_path = f.name
        config.write()

        with open(f.name, 'r') as written_config_fp:
            loaded_config = json.load(written_config_fp)
        self.assertEqual(json.loads(config_string), loaded_config)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    @data_provider(config_fixtures)
    def test_write_config_failure(self, config_string, check_paths, expected_config_path):
        config = PolypyConfig()
        config.config = json.loads(config_string)


if __name__ == '__main__':
    unittest.main()
