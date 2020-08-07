import sys
import io
import unittest
import unittest.mock

from poly_py_tools.config_writer import ConfigWriter
from poly_py_tools.polypy_config import PolypyConfig
from unittest_data_provider import data_provider

class TestConfigWriter(unittest.TestCase):

    def test_use(self):
        writer = ConfigWriter()
        writer.use("thisdevice")
        self.assertEqual("thisdevice", writer.device)

    def test_set_verbosity(self):
        writer = ConfigWriter()
        writer.set_verbosity(9)

        self.assertEqual(9, writer.verbosity)

    def test_use_configs(self):
        writer = ConfigWriter()
        writer.use_configs("asdf")
        self.assertEqual("asdf", writer.configs)

    provider_test_log = lambda: (
        ( "871737ba-6308-492d-a115-4eb41d7a9501", 0, 1, ""),
        ( "a9420e2f-4d02-45e2-bb2a-b5a018e2e537", 1, 1, "a9420e2f-4d02-45e2-bb2a-b5a018e2e537\n"),
        ( "033fa2d6-0ace-4dbc-926c-4e6a957f968e", 1, 2, ""),
        ( "eaec83c2-67bf-4790-aab4-4b48e995a945", 1, 9, ""),
        ( "eaec83c2-67bf-4790-aab4-4b48e995a945", 9, 5, "eaec83c2-67bf-4790-aab4-4b48e995a945\n"),
        ( "2f19d9d2-5ff5-45c3-a747-0f770cf561d5", 9, 1, "2f19d9d2-5ff5-45c3-a747-0f770cf561d5\n"),
        ( "cc866eb0-201a-495e-b83e-3c4ddb8c6348", 9, 0, "cc866eb0-201a-495e-b83e-3c4ddb8c6348\n"),
    )
    
    @data_provider(provider_test_log)
    def test_log(self, message, current_verbosity_level, minimum_verbosity_level, expected_output):
        writer = ConfigWriter()
        writer.set_verbosity(current_verbosity_level)
        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        writer.log(message, minimum_verbosity_level)
        output = out.getvalue()

        self.assertEqual(expected_output, output)
