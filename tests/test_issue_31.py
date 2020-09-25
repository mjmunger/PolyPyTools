import unittest
import os
import sys
from shutil import copy
from shutil import rmtree
from unittest.mock import MagicMock
from docopt import docopt

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.provision_factory import ProvisionFactory
from xml.etree import ElementTree as ET


class TestIssue31(unittest.TestCase):

    def setUp(self) -> None:

        if not os.path.exists(self.issue_asterisk()):
            os.mkdir(self.issue_asterisk())

        if not os.path.exists(self.issue_tftproot()):
            os.mkdir(self.issue_tftproot())

        pjsip_src = os.path.join(self.issue_base(), "pjsip.conf")
        pjsip_dst = os.path.join(self.issue_asterisk(), "pjsip.conf")
        copy(pjsip_src, pjsip_dst)


    # def tearDown(self) -> None:
    #     if os.path.exists(self.issue_asterisk()):
    #         rmtree(self.issue_asterisk())
    #
    #     if os.path.exists(self.issue_tftproot()):
    #         rmtree(self.issue_tftproot())

    def test_issue_31(self):
        argv = "polypy provision polycom 0004F2E62AA4".split(" ")
        sys.argv = argv

        from poly_py_tools.provision import provision
        args = docopt(provision.__doc__)

        issue_base = self.issue_base()

        pconf = PolypyConfig()
        pconf.add_search_path(issue_base)
        pconf.find()
        pconf.load()

        # Redirect output, etc... to issue_31 tmp directory
        pconf.set_path("asterisk", self.issue_asterisk())
        pconf.set_path('tftproot', self.issue_tftproot())

        self.assertTrue(os.path.exists(pconf.pjsip_path()))

        args['pconf'] = pconf
        args['<args>'] = args

        # Patch the generator to redirect firmware lookup to the fixture directory.
        meta = ModelMeta()
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))
        args['meta'] = meta

        sip_resource_factory = SipResourceFactory()
        factory = ProvisionFactory()
        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(sip_resource_factory)

        args['pjsipsectionparser'] = parser
        runner = factory.get_runner(args)
        print(runner)
        runner.run()

        tree = ET.parse(os.path.join(self.issue_tftproot(), "com-l-3-office/0004f2e62aa4"))
        root = tree.getroot()

        self.assertEqual("polycomConfig", root.tag)

        reg = root.find("reg")
        addr = reg.attrib['reg.1.address']
        buffer = addr.split("@")
        self.assertEqual(buffer[1], "pbx.example.org", "reg.1.address should have pbx.hph.io as the server, found '{}' instead.".format(buffer[1]))

    def issue_base(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_31")

    def issue_asterisk(self):
        return os.path.join(self.issue_base(), "asterisk")

    def issue_tftproot(self):
        return os.path.join(self.issue_base(), "tftproot")
