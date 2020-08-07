import unittest
from unittest_data_provider import data_provider
from poly_py_tools.provision_factory import ProvisionFactory
from poly_py_tools.provision.provision_polycom import ProvisionPolycom


class TestProvisionFactory(unittest.TestCase):

    provider_test_factory = lambda : (
        ({'polycom': True, '<macaddress>': 'asdf'}, 'PolycomProvision'),
    )

    @data_provider(provider_test_factory)
    def test_get_runner(self, args, expected_class):
        self.skipTest("Not developed yet")
        factory = ProvisionFactory()
        runner = factory.get_runner(args)
        self.assertTrue(isinstance(runner, expected_class))

