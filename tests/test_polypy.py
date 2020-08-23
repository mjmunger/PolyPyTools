import sys
import unittest
import os
import io
from pprint import pprint
from unittest.mock import patch
from docopt import DocoptExit
from poly_py_tools.docopt_extractor import DocoptExtractor
from unittest_data_provider import data_provider
from poly_py_tools.polypy import Polypy


class TestPolypy(unittest.TestCase):

    provider_test_polypy_commands = lambda : (
        ({'--force': False,
          '-d': True,
          '-h': False,
          '-v': 0,
          '<args>': [],
          '<command>': 'sip'}, 'sip_manager.py'),

    )

    @data_provider(provider_test_polypy_commands)
    def test_polypy_commands(self, args, imported_file):
        lib_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'poly_py_tools')
        self.assertTrue(os.path.exists(lib_path))
        doe = DocoptExtractor(lib_path)
        expected_message = doe.docopt(imported_file)

        polypy = Polypy(args)

        self.assertEqual(args, polypy.args)
        error_message = doe.docopt(imported_file)
        with patch("builtins.SystemExit"):
            with self.assertRaises(DocoptExit) as cm:
                try:
                    polypy.run()
                except DocoptExit:
                    pass
                pprint(cm.format_message)







if __name__ == '__main__':
    unittest.main()
