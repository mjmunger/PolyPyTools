import unittest
import sys
import os
import io
from unittest_data_provider import data_provider
from poly_py_tools.polycom_provision import PolycomProvision
from poly_py_tools.provision_factory import ProvisionFactory
from poly_py_tools.provision.provision_lister import ProvisionLister

from poly_py_tools.pjsip_section_parser import PjSipSectionParser

class TestPolypyProvision(unittest.TestCase):

    provider_test_polycom = lambda : (
        ({'polycom': True, '<macaddress>': 'asdf', 'list': False, 'templates': False, 'endpoints': False, 'all': False}, PolycomProvision),
        ({'polycom': False, '<macaddress>': False, 'list': True, 'templates': True, 'endpoints': False, 'all': False}, ProvisionLister),
        ({'polycom': False, '<macaddress>': False, 'list': True, 'templates': False, 'endpoints': True, 'all': False}, ProvisionLister),
        ({'polycom': False, '<macaddress>': False, 'list': True, 'templates': False, 'endpoints': False, 'all': True}, ProvisionLister),
        ({'polycom': False, '<macaddress>': "D9:72:4E:31:63:94", 'list': False, 'templates': False, 'endpoints': False, 'all': False, '<csvfile>': os.path.join(os.getcwd(), "fixtures/csvfiles/file1.csv"), 'directory': True, 'using': True}, ProvisionDirectory),
    )

    @data_provider(provider_test_polycom)
    def test_polycom(self, args, expected_class):
        factory = ProvisionFactory()
        runner = factory.get_runner(args)
        self.assertTrue(isinstance(runner, expected_class))

    def test_list_devices(self):
        config = {"paths" : {'asterisk': os.path.join(os.getcwd(), 'fixtures/pjsip/')}}
        args = {'polycom': False, '<macaddress>': False, 'list': True, 'templates': True, 'devices': False, 'all': False, 'config' : config}
        lister = ProvisionLister(args)
        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        lister.run()
        output = out.getvalue()

        self.assertEqual("Endpoints found in pjsip.conf:\n6001 (0004f23a43bf)\n6002\nbandwidth_cloud\n", output)