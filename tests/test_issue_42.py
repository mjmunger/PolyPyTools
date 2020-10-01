import io
import os
import sys
from unittest.mock import MagicMock

from docopt import docopt
from shutil import rmtree
import unittest

from pwgen_secure.rpg import Rpg

from poly_py_tools.pjsip.pjsip import PJSip
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.provision import Provision

from xml.etree import ElementTree as ET

class TestIssue39(unittest.TestCase):

    def asterisk_path(self):
        return os.path.join(self.issue_root(), "asterisk")

    def tftproot_path(self):
        return os.path.join(self.issue_root(), "tftproot")

    def issue_root(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_39/")

    def setUp(self) -> None:
        if not os.path.exists(self.tftproot_path()):
            os.mkdir(self.tftproot_path())

        if not os.path.exists(self.asterisk_path()):
            os.mkdir(self.asterisk_path())

    def tearDown(self) -> None:
        if os.path.exists(self.tftproot_path()):
            rmtree(self.tftproot_path())

        if os.path.exists(self.asterisk_path()):
            rmtree(self.asterisk_path())

    def test_issue_39(self):
        # <setup command and args>
        argv = "polypy pjsip generate 111 from {} with voicemail".format(os.path.join(self.issue_root(), "DialPlanBuilder.csv")).split(" ")
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
        pconf.add_search_path(self.issue_root())
        pconf.load()
        pconf.set_path("asterisk", self.asterisk_path())
        pconf.set_path("tftproot", self.tftproot_path())
        container['pconf'] = pconf

        # <setup container>

        # <setup stdio>
        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        # <setup stdio>

        # <run>
        pjsip = PJSip(container)
        pjsip.run()
        # </run>

        # <assertions>
        f = open(os.path.join(self.issue_root(), "expected_pjsip.conf"), 'r')
        buffer = f.read()
        f.close()
        expected_conf = "".join(buffer)

        f = None
        buffer = None

        f = open(os.path.join(self.asterisk_path(), "pjsip.conf"), 'r')
        buffer = f.read()
        f.close()
        actual_conf = "".join(buffer)

        self.assertEqual(expected_conf, actual_conf)
        # </assertions>


if __name__ == '__main__':
    unittest.main()
