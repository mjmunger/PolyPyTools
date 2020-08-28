import unittest
import os
import json
import shutil
from unittest.mock import patch, mock_open, MagicMock

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.provision_polycom import ProvisionPolycom


class TestProvisionPolycom(unittest.TestCase):

    def get_args(self):
        pconf = PolypyConfig()

        f = open(os.path.join(os.path.dirname(__file__), 'fixtures/base_config.json'))
        configs = json.load(f)
        f.close()

        configs['paths']['tftproot'] = "/tmp/"
        configs['paths']['asterisk'] = os.path.join(os.path.dirname(__file__), "fixtures/pjsip/")

        pconf.json = configs

        args = {'--force': False,
                '-d': True,
                '-v': 0,
                '<csvfile>': [],
                '<macaddress>': '0004f23a43bf',
                'directory': False,
                'endpoints': False,
                'for': False,
                'list': False,
                'polycom': True,
                'provision': True,
                'using': False}

        args['pconf'] = pconf

        return args

    def test_init(self):

        args = self.get_args()
        meta = ModelMeta()
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))
        args['meta'] = meta
        args['sip_factory'] = SipResourceFactory()

        PP = ProvisionPolycom(args)
        self.assertEqual(args, PP.args)
        self.assertEqual(args['pconf'].configs(), PP.configs)


    def test_run(self):
        """
        Confirm ProvisionPolycom does the following:
        1. Creates the bootstrap file
        2. Creates the configuration file
        3. Outputs what it did to the screen

        We don't worry about content here because the Endpoint class is the class responsible for content.
        :return:
        """

        args = self.get_args()
        meta = ModelMeta()
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))
        args['meta'] = meta
        args['sip_factory'] = SipResourceFactory()

        sip_factory = SipResourceFactory()
        if args['-d']:
            sip_factory.set_debug()

        parser = PjSipSectionParser()
        parser.use_config(args['pconf'])
        parser.use_factory(sip_factory)

        args['pjsipsectionparser'] = parser


        PP = ProvisionPolycom(args)

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

        PP.run()

        self.assertTrue(os.path.exists("/tmp/some-site-template/"), "/tmp/some-site-template/ should exist, but does not.")
        for target_file in target_files:
            self.assertTrue(os.path.exists(target_file), "{} should exist, but does not.".format(target_file))


if __name__ == '__main__':
    unittest.main()
