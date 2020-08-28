import os
import unittest
from unittest.mock import MagicMock

from unittest_data_provider import data_provider

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.provision_directory import ProvisionDirectory
from poly_py_tools.provision.provision_lister import ProvisionLister
from poly_py_tools.provision_factory import ProvisionFactory
from poly_py_tools.provision.provision_polycom import ProvisionPolycom


class TestProvisionFactory(unittest.TestCase):

    provider_test_factory = lambda : (
        ({'polycom': True, '<macaddress>': 'asdf', 'config' : []}, ProvisionPolycom),
        ({'--force': False,
         '-d': False,
         '-v': 0,
         '<csvfile>': [],
         '<macaddress>': None,
         'directory': False,
         'endpoints': True,
         'for': False,
         'list': True,
         'polycom': False,
         'provision': True,
         'using': False,
          'config' : []}, ProvisionLister),
        ({'--force': False,
         '-d': False,
         '-v': 0,
         '<csvfile>': ['somefile.csv'],
         '<macaddress>': 'asdf',
         'directory': True,
         'endpoints': False,
         'for': True,
         'list': False,
         'polycom': False,
         'provision': True,
         'using': True,
        'config' : []},  ProvisionDirectory)
    )

    @data_provider(provider_test_factory)
    def test_get_runner(self, args, expected_class):
        meta = ModelMeta()
        # meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))
        args['meta'] = meta
        args['sip_factory'] = SipResourceFactory()
        pconf = PolypyConfig()
        args['pconf'] = pconf
        provision_factory = ProvisionFactory()
        runner = provision_factory.get_runner(args)
        self.assertTrue(isinstance(runner, expected_class))

