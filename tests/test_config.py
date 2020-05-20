import unittest
import os.path

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
        self.assertEqual(exists, config.find(check_paths))
        self.assertEqual(expected_config_path, config.config_path)


if __name__ == '__main__':
    unittest.main()
