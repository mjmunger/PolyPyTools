import unittest

from unittest_data_provider import data_provider

from poly_py_tools.pjsip.pjsip_generator import PJSipGenerator
from poly_py_tools.pjsip.pjsip_factory import PJSipFactory


class TestPJSipFactory(unittest.TestCase):

    provider_test_get_runner = lambda : (
        ({'--force': False,
         '-d': True,
         '-v': 0,
         '<column>': None,
         '<extension>': '111',
         '<file>': 'DialPlanBuilder-L3_pbx_v1.csv',
         '<template>': None,
         'assign': False,
         'column': False,
         'from': True,
         'generate': True,
         'pjsip': True,
         'template': False,
         'use': False,
         'voicemail': False,
         'with': False }, PJSipGenerator),
    )

    @data_provider(provider_test_get_runner)
    def test_get_runner(self, args, expected_class):
        container = {}
        container['args'] = args
        factory = PJSipFactory()
        runner = factory.get_runner(container)
        self.assertTrue(isinstance(runner, expected_class))


if __name__ == '__main__':
    unittest.main()
