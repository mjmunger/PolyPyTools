import unittest
from unittest_data_provider import data_provider
from poly_py_tools.polycom_provision import PolycomProvision
from poly_py_tools.pjsip_section_parser import PjSipSectionParser

class TestPolypyProvision(unittest.TestCase):

    provider_test_polycom = lambda : (
        ({'polycom': True, '<macaddress>': 'asdf'}, 'PolycomProvision'),
    )

    @data_provider(provider_test_polycom)
    def test_polycom(self, args, expected_class):
        factory = ProvisionFactory()
        runner = factory.getRunner(args)
        self.assertTrue(isinstance(runner, expected_class))

