import unittest
import os
from shutil import copy
from shutil import rmtree
from unittest.mock import MagicMock

from unittest_data_provider import data_provider

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy import Polypy
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision_factory import ProvisionFactory
from xml.etree import ElementTree as ET



class TestIssue31(unittest.TestCase):

    def setUp(self) -> None:

        self.clean_files()
        prep_directories = self.get_prep_directories()
        pjsip_src = os.path.join(self.issue_base(), "pjsip.conf")
        pjsip_dst = os.path.join(prep_directories['asterisk'], "pjsip.conf")
        copy(pjsip_src, pjsip_dst)

    def clean_files(self):
        prep_directories = self.get_prep_directories()

        for dir in prep_directories:
            target_directory = os.path.join(self.issue_base(), dir)
            # print("Target directory: {}".format(target_directory))
            for f in os.listdir(target_directory):
                target_file = os.path.join(target_directory, f)
                if not os.path.isdir(target_file):
                    os.remove(target_file)

        rmtree(os.path.join(prep_directories['tftproot'], "com-l-3-office"))

    def get_prep_directories(self):
        prep_directories = {}
        asterisk_dir = os.path.join(self.issue_base(), "asterisk")
        tftproot_dir = os.path.join(self.issue_base(), "tftproot")
        prep_directories['asterisk'] = asterisk_dir
        prep_directories['tftproot'] = tftproot_dir

        return prep_directories

    def tearDown(self) -> None:
        self.clean_files()

    def test_issue_31(self):
        args = {'--force': False,
                 '-d': False,
                 '-v': 0,
                 '<csvfile>': [],
                 '<macaddress>': '0004F2E62AA4',
                 'directory': False,
                 'endpoints': False,
                 'for': False,
                 'list': False,
                 'polycom': True,
                 'provision': True,
                 'using': False}

        issue_base = self.issue_base()

        pconf = PolypyConfig()
        pconf.add_search_path(issue_base)
        pconf.find()
        pconf.load()

        # Redirect output, etc... to issue_31 tmp directory
        pconf.update_paths("asterisk", os.path.join(issue_base, "asterisk"))
        pconf.update_paths("tftproot", os.path.join(issue_base, "tftproot"))

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
        runner.run()

        tree = ET.parse(os.path.join(pconf.tftproot_path(), "com-l-3-office/0004f2e62aa4"))
        root = tree.getroot()

        self.assertEqual("polycomConfig", root.tag)

        reg = root.find("reg")
        addr = reg.attrib['reg.1.address']
        buffer = addr.split("@")
        self.assertEqual(buffer[1], "pbx.example.org", "reg.1.address should have pbx.hph.io as the server, found '{}' instead.".format(buffer[1]))

    def issue_base(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_31")