import unittest
from unittest_data_provider import data_provider
from poly_py_tools.provision_factory import ProvisionFactory
from poly_py_tools.polycom_provision import PolycomProvision


class TestProvisionFactory(unittest.TestCase):

    provider_test_factory = lambda : (
        ({'polycom': True, '<macaddress>': 'asdf'}, 'PolycomProvision'),
    )

    @data_provider(provider_test_factory)
    def test_get_runner(self, args, expected_class):
        factory = ProvisionFactory()
        runner = factory.getRunner(args)
        self.assertTrue(isinstance(runner, expected_class))

