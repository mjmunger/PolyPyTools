import os
import sys
from unittest.mock import MagicMock

from docopt import docopt
from shutil import rmtree
import unittest

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.provision import Provision

from xml.etree import ElementTree as ET

class TestIssue36(unittest.TestCase):

    def asterisk_path(self):
        return os.path.join(self.issue_root(), "asterisk")

    def tftproot_path(self):
        return os.path.join(self.issue_root(), "tftproot")

    def issue_root(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_36/")

    def setUp(self) -> None:
        if not os.path.exists(self.tftproot_path()):
            os.mkdir(self.tftproot_path())

    def tearDown(self) -> None:
        if os.path.exists(self.tftproot_path()):
            rmtree(self.tftproot_path())

    def test_issue_36(self):

        # Setup like we do in polypy.py

        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(self.issue_root())
        pconf.find()
        pconf.load()
        container['pconf'] = pconf

        sip_resource_factory = SipResourceFactory()

        section_parser = PjSipSectionParser()
        section_parser.use_config(pconf)
        section_parser.use_factory(sip_resource_factory)

        container['pjsipsectionparser'] = section_parser

        # End setup.

        # Begin mocks and test setup.
        meta = ModelMeta()
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/"))
        meta.use_configs(pconf)
        container['meta'] = meta

        container['pconf'].set_path('asterisk',self.asterisk_path())
        container['pconf'].set_path('tftproot',self.tftproot_path())

        argv = "polypy provision polycom 0004f2e62aa4".split(" ")
        sys.argv = argv

        # /end mocks

        from poly_py_tools.provision import provision
        container['<args>'] = docopt(provision.__doc__)
        provision = Provision(container)
        provision.run()

        # Begin assertions

        # There should be TWO registrations

        tree = ET.parse(os.path.join(pconf.tftproot_path(), "com-l-3-office/0004f2e62aa4"))
        root = tree.getroot()

        self.assertEqual("polycomConfig", root.tag)

        reg = root.find("reg")

        reg_1_address = reg.attrib['reg.1.address']
        reg_1_password = reg.attrib['reg.1.auth.password']
        reg_1_userid = reg.attrib['reg.1.auth.userId']
        reg_1_label = reg.attrib['reg.1.label']

        expected_reg_1_address = "0004f2e62aa4111@pbx.hph.io"
        expected_reg_1_password = "DuolOou9ioFzYM6J"
        expected_reg_1_userid = "0004f2e62aa4111"
        expected_reg_1_label = "Line 1"

        self.assertEqual(expected_reg_1_address, reg_1_address)
        self.assertEqual(expected_reg_1_password, reg_1_password)
        self.assertEqual(expected_reg_1_userid, reg_1_userid)
        self.assertEqual(expected_reg_1_label, reg_1_label)

        reg_2_address = reg.attrib['reg.2.address']
        reg_2_password = reg.attrib['reg.2.auth.password']
        reg_2_userid = reg.attrib['reg.2.auth.userId']
        reg_2_label = reg.attrib['reg.2.label']

        expected_reg_2_address = "0004f2e62aa4104@pbx.hph.io"
        expected_reg_2_password = "Sc7mUrBUeFZO890I"
        expected_reg_2_userid = "0004f2e62aa4104"
        expected_reg_2_label = "Line 2"

        self.assertEqual(expected_reg_2_address, reg_2_address)
        self.assertEqual(expected_reg_2_password, reg_2_password)
        self.assertEqual(expected_reg_2_userid, reg_2_userid)
        self.assertEqual(expected_reg_2_label, reg_2_label)

if __name__ == '__main__':
    unittest.main()
