import shutil
import sys
import unittest
import os
from docopt import docopt

from poly_py_tools.polypy_config import PolypyConfig
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

    def test_site(self):

        argv = "polypy site init example.org".split(" ")
        sys.argv = argv

        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(TestSite.issue_root())
        pconf.find()
        pconf.load()

        container['pconf'] = pconf

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions
        site.run()

        # Post run assertions
        self.assertTrue(os.path.exists(os.path.join(TestSite.issue_tftproot(), 'org.example')))




if __name__ == '__main__':
    unittest.main()
