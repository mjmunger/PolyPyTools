import sys
import unittest
import os
from shutil import rmtree
from shutil import copy
from docopt import docopt
from pwgen_secure.rpg import Rpg

from poly_py_tools.pjsip.pjsip_factory import PJSipFactory
from poly_py_tools.polypy_config import PolypyConfig


class TestIssue29(unittest.TestCase):
    def asterisk_path(self):
        return os.path.join(self.issue_root(), "asterisk")

    def tftproot_path(self):
        return os.path.join(self.issue_root(), "tftproot")

    def issue_root(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator/")

    def setUp(self) -> None:
        if not os.path.exists(self.tftproot_path()):
            os.mkdir(self.tftproot_path())

        if not os.path.exists(self.asterisk_path()):
            os.mkdir(self.asterisk_path())

    def tearDown(self) -> None:
        if os.path.exists(self.tftproot_path()):
            rmtree(self.tftproot_path())

    def test_issue_29(self):

        fixture_path = os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator")
        csv_path = os.path.join(fixture_path, )

        argv = "polypy pjsip generate 111 from {}".format(os.path.join(self.issue_root(), 'DialPlanBuilder-ExampleOrg.csv')).split(" ")
        sys.argv = argv
        from poly_py_tools.pjsip import pjsip
        args = docopt(pjsip.__doc__)

        pconf = PolypyConfig()
        pconf.add_search_path(self.issue_root())
        pconf.load()
        container = {}
        container['pconf'] = pconf

        container['pconf'] = pconf
        container['args'] = args
        container['rpg'] = Rpg("strong", None)

        factory = PJSipFactory()
        runner = factory.get_runner(container)
        runner.run()


if __name__ == '__main__':
    unittest.main()
