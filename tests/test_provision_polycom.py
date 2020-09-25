import unittest
import os
import json
import shutil
import sys
from unittest.mock import patch, mock_open, MagicMock
from docopt import docopt

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.provision_polycom import ProvisionPolycom


class TestProvisionPolycom(unittest.TestCase):

    def get_container(self):
        pconf = PolypyConfig()

        f = open(os.path.join(os.path.dirname(__file__), 'fixtures/base_config.json'))
        configs = json.load(f)
        f.close()

        configs['paths']['tftproot'] = "/tmp/"
        configs['paths']['asterisk'] = os.path.join(os.path.dirname(__file__), "fixtures/pjsip/")

        pconf.json = configs

        argv = "polypy provision polycom 0004f23a43bf".split(" ")
        sys.argv = argv
        from poly_py_tools.provision import provision
        args = docopt(provision.__doc__)
        container = {}
        container['pconf'] = pconf
        container['<args>'] = args

        return container

    def test_init(self):

        container = self.get_container()
        meta = ModelMeta()
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs"))
        container['meta'] = meta
        container['sip_factory'] = SipResourceFactory()

        provision_polycom = ProvisionPolycom(container)
        self.assertEqual(container, provision_polycom.container)
        self.assertEqual(container['pconf'].configs(), provision_polycom.configs)


    def test_run(self):
        """
        Confirm ProvisionPolycom does the following:
        1. Creates the bootstrap file
        2. Creates the configuration file
        3. Outputs what it did to the screen

        We don't worry about content here because the Endpoint class is the class responsible for content.
        :return:
        """

        container = self.get_container()

        meta = ModelMeta()
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))
        container['meta'] = meta
        container['sip_factory'] = SipResourceFactory()

        sip_factory = SipResourceFactory()

        parser = PjSipSectionParser()
        parser.use_config(container['pconf'])
        parser.use_factory(sip_factory)

        container['pjsipsectionparser'] = parser

        provision_polycom = ProvisionPolycom(container)

        target_files = ["/tmp/some-site-template/0004f23a43bf", "/tmp/0004f23a43bf.cfg"]
        for target_file in target_files:
            if os.path.exists(target_file):
                os.remove(target_file)

        if os.path.exists("/tmp/some-site-template/"):
            os.rmdir("/tmp/some-site-template/")

        self.assertFalse(os.path.exists("/tmp/some-site-template/"))

        for target_file in target_files:
            self.assertFalse(os.path.exists(target_file))

        firmware_src_dir = os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/4.0.15.1009/Config")
        target_firmware_dir = "/tmp/firmware/4.0.15.1009/Config/"

        if not os.path.exists(target_firmware_dir):
            os.makedirs(target_firmware_dir)

        reg_basic_src = os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/4.0.15.1009/Config/reg-basic.cfg")

        target_reg_basic = os.path.join(target_firmware_dir, "reg-basic.cfg")

        if not os.path.exists(target_reg_basic):
            shutil.copyfile(reg_basic_src, target_reg_basic)

        f = open(os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/4.0.15.1009/Config/reg-basic.cfg"))
        config = f.read()
        f.close()

        provision_polycom.run()

        self.assertTrue(os.path.exists("/tmp/some-site-template/"), "/tmp/some-site-template/ should exist, but does not.")
        for target_file in target_files:
            self.assertTrue(os.path.exists(target_file), "{} should exist, but does not.".format(target_file))


if __name__ == '__main__':
    unittest.main()
