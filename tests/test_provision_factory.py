import unittest
from unittest_data_provider import data_provider

from poly_py_tools.polypy_config import PolypyConfig
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
        pconf = PolypyConfig()
        args['config'] = pconf
        factory = ProvisionFactory()
        runner = factory.get_runner(args)
        self.assertTrue(isinstance(runner, expected_class))

