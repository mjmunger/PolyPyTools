import sys
import os
import io
import unittest
from shutil import rmtree, copy
from docopt import docopt
from unittest import mock
from unittest.mock import patch, mock_open, MagicMock
from unittest_data_provider import data_provider

from poly_py_tools.dialplan import Dialplan
from poly_py_tools.pjsip.pjsip_generator import PJSipGenerator
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from pwgen_secure.rpg import Rpg

class MockOpenWrite:

    buffer = []

    def __init__(self, *args, **kwargs):
        self.buffer = []
    # What's actually mocking the write. Name must match
    def write(self, s: str):
        self.res.append(s)
    # These 2 methods are needed specifically for the use of with.
    # If you mock using a decorator, you don't need them anymore.
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return
    def read_back(self):
        return "\n".join(self.buffer)


class TestPJSipGenerator(unittest.TestCase):

    def issue_root(self):
        return os.path.join(os.path.dirname(__file__),"fixtures/pjsip_generator")

    def issue_asterisk(self):
        return os.path.join(self.issue_root(), "asterisk")

    def issue_tftproot(self):
        return os.path.join(self.issue_root(), "tftproot")

    def setUp(self) -> None:
        if not os.path.exists(self.issue_asterisk()):
            os.mkdir(self.issue_asterisk())

        if not os.path.exists(self.issue_tftproot()):
            os.mkdir(self.issue_tftproot())

    # def tearDown(self) -> None:
    #     if os.path.exists(self.issue_tftproot()):
    #         rmtree(self.issue_tftproot())
    #
    #     if os.path.exists(self.issue_asterisk()):
    #         rmtree(self.issue_asterisk())

    def test_init(self):
        container = {}
        mock_rpg = Rpg("strong", None)
        mock_rpg.generate_password = MagicMock(return_value="QoWTIllrgkVKZR")
        container['rpg'] = mock_rpg

        pconf = PolypyConfig()
        container['pconf'] = pconf

        generator = PJSipGenerator(container)
        self.assertEqual(container, generator.container)
        self.assertEqual(pconf, generator.pconf)
        self.assertEqual(mock_rpg, generator.rpg)

    def base_config(self):
        return {"lib_path":"/var/lib/polypy","share_path":"/usr/share/polypy/","config_path":"","package_path":"/usr/local/lib/python3.7/dist-packages/poly_py_tools","server_addr":"pbx.example.org","paths":{"asterisk":"","tftproot":""}}

    def test_use(self):
        container = {}
        mock_rpg = Rpg("strong", None)
        mock_rpg.generate_password = MagicMock(return_value="QoWTIllrgkVKZR")
        container['rpg'] = mock_rpg

        pconf = PolypyConfig()
        container['pconf'] = pconf

        generator = PJSipGenerator({})
        generator.use(container)
        self.assertEqual(container, generator.container)
        self.assertEqual(pconf, generator.pconf)
        self.assertEqual(mock_rpg, generator.rpg)

    @mock.patch("os.path")
    def test_generate_from_file_exists(self, mock_path):

        generator = PJSipGenerator({})
        existing_file = "/this/file/exists"

        mock_path.exists = lambda path : True
        generator.generate_from(existing_file)
        self.assertEqual(existing_file, generator.source_csv)

    @mock.patch("os.path")
    def test_generate_from_file_not_exists(self, mock_path):
        non_existant_file = "/this/file/does/not/exist"
        generator = PJSipGenerator({})

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

        container = {}
        container['pconf'] = config
        container['rpg'] = mock_rpg
        container['args'] = {'<extension>': "1001"}

        dialplan = Dialplan(csv_path)
        dialplan.with_config(config)
        dialplan.parse()

        generator = PJSipGenerator(container)
        # self.assertRaises(ValueError, generator.generate_from(csv_path))
        # generator.use(config)
        # generator.with_rpg(mock_rpg)
        generator.generate_from(csv_path)
        generator.parse_dialplan(dialplan)
        self.assertEqual(expected_configs, generator.render_conf())

    provider_test_generator = lambda: (
        ( 'DialPlanBuilder-ExampleOrg.csv', 'expected_pjsip_01.conf'),
    )

    @data_provider(provider_test_generator)
    def test_run(self, csv, expected_conf):
        # <setup command and args>

        argv = "polypy pjsip generate 1001 from {} with voicemail".format(
            os.path.join(self.issue_root(), "DialPlanBuilder-ExampleOrg.csv")).split(" ")
        sys.argv = argv
        from poly_py_tools.pjsip import pjsip
        args = docopt(pjsip.__doc__)

        # </setup command and args>

        # <setup container>
        container = {}

        container['args'] = args
        mock_rpg = Rpg("strong", None)
        mock_rpg.generate_password = MagicMock(return_value="QoWTIllrgkVKZR")
        container['rpg'] = mock_rpg

        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator/"))
        pconf.load()
        pconf.set_path("asterisk", self.issue_asterisk())

        container['pconf'] = pconf

        # </setup container>

        # <setup stdio>
        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        # <setup stdio>

        # <run>

        generator = PJSipGenerator(container)
        generator.run()
        output = out.getvalue()

        # </run>

        # <assertions>
        expected_conf_path = os.path.join(self.issue_root(), "expected_pjsip_01.conf")

        f = open(expected_conf_path, 'r')
        buffer = f.read()
        f.close()
        expected_configs = "".join(buffer)

        target_output_file = os.path.join(self.issue_asterisk(), "pjsip.conf")
        self.assertTrue(os.path.exists(target_output_file))

        self.assertEqual("Saved to: {}\n".format(target_output_file), output)
        self.assertTrue(os.path.exists(target_output_file))

        f = open(target_output_file, 'r')
        buffer = f.read()
        f.close()

        self.assertEqual(expected_configs, "".join(buffer))
        # </assertions>

    def test_append(self):
        csv = "DialPlanBuilder-ExampleOrg.csv"
        expected_conf = "expected_pjsip_02.conf"
        # <setup command and args>

        argv = "polypy -a pjsip generate 1002 from {} with voicemail".format(
            os.path.join(self.issue_root(), "DialPlanBuilder-ExampleOrg.csv")).split(" ")
        sys.argv = argv
        from poly_py_tools.pjsip import pjsip
        args = docopt(pjsip.__doc__)

        # </setup command and args>

        # <setup files>
        src = os.path.join(self.issue_root(),"expected_pjsip_01.conf")
        dst = os.path.join(self.issue_asterisk(), "pjsip.conf")
        copy(src, dst)
        # </setup files>

        # <setup container>
        container = {}

        container['args'] = args
        mock_rpg = Rpg("strong", None)
        mock_rpg.generate_password = MagicMock(return_value="QoWTIllrgkVKZR")
        container['rpg'] = mock_rpg

        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator/"))
        pconf.load()
        pconf.set_path("asterisk", self.issue_asterisk())

        container['pconf'] = pconf

        factory = SipResourceFactory()
        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(factory)
        container['pjsipparser'] = parser

        # </setup container>

        # <setup stdio>
        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        # <setup stdio>

        # <run>

        generator = PJSipGenerator(container)
        generator.run()
        output = out.getvalue()

        # </run>

        # <assertions>
        expected_conf_path = os.path.join(self.issue_root(), "expected_pjsip_02.conf")

        f = open(expected_conf_path, 'r')
        buffer = f.read()
        f.close()
        expected_configs = "".join(buffer)

        target_output_file = os.path.join(self.issue_asterisk(), "pjsip.conf")
        self.assertTrue(os.path.exists(target_output_file))

        self.assertEqual("Saved to: {}\n".format(target_output_file), output)
        self.assertTrue(os.path.exists(target_output_file))

        f = open(target_output_file, 'r')
        buffer = f.read()
        f.close()

        self.assertEqual(expected_configs, "".join(buffer))
        # </assertions>
if __name__ == '__main__':
    unittest.main()
