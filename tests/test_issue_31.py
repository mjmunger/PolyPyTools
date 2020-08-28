import unittest
import os
from copy import copy

from unittest_data_provider import data_provider

from poly_py_tools.polypy import Polypy
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision_factory import ProvisionFactory


class TestIssue30(unittest.TestCase):

    def setUp(self) -> None:

        self.clean_files()
        prep_directories = self.get_prep_directories()
        pjsip_src = os.path.join(self.issue_base(), "pjsip.conf")
        pjsip_dst = os.path.join(prep_directories['asterisk'], "pjsip.conf")
        copy(pjsip_src, pjsip_dst)

    def clean_files(self):
        prep_directories = self.get_prep_directories()

        for target_directory in prep_directories:
            for f in target_directory:
                os.remove(f)

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
                 '-d': True,
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
        pconf.json['paths']['asterisk'] = os.path.join(issue_base, "asterisk")
        pconf.json['paths']['tftproot'] = os.path.join(issue_base, "tftproot")

        # Patch the generator to redirect firmware lookup to the fixture directory.


        args['config'] = pconf
        args['<args>'] = args

        factory = ProvisionFactory()
        runner = factory.get_runner(args)
        runner.run()

    def issue_base(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_31")