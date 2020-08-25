import unittest

from unittest_data_provider import data_provider

from poly_py_tools.pjsip.pjsip_generator import PJSipGenerator
from poly_py_tools.pjsip.pjsip_factory import PJSipFactory


class TestPJSipFactory(unittest.TestCase):

    provider_test_get_runner = lambda : (
        ({'--force': False,
         '-d': True,
         '-h': False,
         '-v': 0,
         '<args>': ['generate'],
         '<command>': 'pjsip'} , PJSipGenerator),
    )

    @data_provider(provider_test_get_runner)
    def test_get_runner(self, args, expected_class):
        factory = PJSipFactory()
        runner = factory.get_runner(args)
        self.assertTrue(isinstance(runner, expected_class))


if __name__ == '__main__':
    unittest.main()
