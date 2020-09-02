import shutil
import sys
import unittest
import os
import io
from unittest.mock import MagicMock

from docopt import docopt
from unittest_data_provider import data_provider

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.site.site import Site


class TestSite(unittest.TestCase):

    @staticmethod
    def issue_tftproot():
        return os.path.join(TestSite.issue_root(), 'tftproot')

    def setUp(self) -> None:

        if not os.path.exists(TestSite.issue_tftproot()):
            os.mkdir(TestSite.issue_tftproot())

    def tearDown(self) -> None:
        tftproot = os.path.join(TestSite.issue_root(), 'tftproot')
        if os.path.exists(tftproot):
            shutil.rmtree(tftproot)

    @staticmethod
    def issue_root():
        return os.path.join(os.path.dirname(__file__), 'fixtures/issue_35')

    provider_test_site = lambda : (
        ("polypy site init example.org", "Directory initialized: /Users/michael/py/PolyPyTools/tests/fixtures/issue_35/tftproot/org-example\n", "6.3.0.14929"),
        ("polypy site init example.org SPIP650", "Directory initialized: /Users/michael/py/PolyPyTools/tests/fixtures/issue_35/tftproot/org-example\n", "4.0.15.1009"),
    )
    @data_provider(provider_test_site)
    def test_site_init(self, command : str, expected_output : str , expected_firmware_version):

        argv = command.split(" ")
        sys.argv = argv

        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(TestSite.issue_root())
        pconf.find()
        pconf.load()
        pconf.json['paths']['tftproot'] = os.path.join(TestSite.issue_root(), 'tftproot')

        container['pconf'] = pconf

        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        self.assertEqual(expected_output, output)
        siteroot = os.path.join(TestSite.issue_tftproot(), 'org-example')
        self.assertTrue(os.path.exists(siteroot))

        files = os.listdir(os.path.join(self.issue_root(), "{}/Config".format(expected_firmware_version)))

        for file in files:
            target_file = os.path.join(siteroot, file)
            self.assertTrue(os.path.exists(target_file), "{} should exist in the siteroot, but does not.".format(target_file))

        files = os.listdir(os.path.join(siteroot))

        for file in files:
            target_source_file = os.path.join(self.issue_root(), "{}/Config".format(expected_firmware_version))
            self.assertTrue(os.path.exists(target_source_file))

    provider_test_site_flush = lambda : (
        "polypy site flush configs for example.org", "Configs flushed for /Users/michael/py/PolyPyTools/tests/fixtures/issue_35/tftproot/org-example"
    )

    @data_provider(provider_test_site_flush)
    def test_site_flush(self, command : str, expected_output : str):

        argv = command.split(" ")
        sys.argv = argv

        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(TestSite.issue_root())
        pconf.find()
        pconf.load()
        pconf.json['paths']['tftproot'] = os.path.join(TestSite.issue_root(), 'tftproot')

        container['pconf'] = pconf

        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        self.assertEqual(expected_output, output)






if __name__ == '__main__':
    unittest.main()
