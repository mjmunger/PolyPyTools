import sys
import unittest
import os
import io
from pprint import pprint
from unittest.mock import patch
from docopt import DocoptExit
from builtins import SystemExit
from poly_py_tools.docopt_extractor import DocoptExtractor
from unittest_data_provider import data_provider
from poly_py_tools.polypy import Polypy

#
# class TestPolypy(unittest.TestCase):
#
#     provider_test_polypy_commands = lambda : (
#         ({'--force': False,
#          '-d': False,
#          '-h': False,
#          '-v': 0,
#          '<args>': [],
#          '<command>': 'provision'}, 'provision/provision.py'),
#         ({'--force': False,
#          '-d': False,
#          '-h': False,
#          '-v': 0,
#          '<args>': [],
#          '<command>': 'pjsip'}, 'pjsip/pjsip.py')
#
#     )
#
#     @data_provider(provider_test_polypy_commands)
#     def test_polypy_commands(self, args, imported_file):
#         lib_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'poly_py_tools')
#         self.assertTrue(os.path.exists(lib_path))
#         doe = DocoptExtractor(lib_path)
#         expected_message = doe.docopt(imported_file)
#
#         polypy = Polypy(args)
#
#         self.assertEqual(args, polypy.args)
#         error_message = doe.docopt(imported_file)
#
#         with self.assertRaises(SystemExit) as cm:
#             polypy.run()
#         self.assertEqual(expected_message, str(cm.exception))
#
#
# if __name__ == '__main__':
#     unittest.main()
