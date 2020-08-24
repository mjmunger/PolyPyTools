import unittest
import os

from unittest_data_provider import data_provider
from poly_py_tools.docopt_extractor import DocoptExtractor


class TestDocOptExtractor(unittest.TestCase):

    provider_test_extract_doctopt = lambda : (
        ('configure/configure.py', 'expected_docopt_for_polypy_configure.py.txt'),
        ('sip_manager.py', 'expected_docopt_for_polypy_sip_manager.py.txt'),
    )

    @data_provider(provider_test_extract_doctopt)
    def test_extract_docopt(self, file_under_test, expected_docopt):
        lib_path = os.path.join(os.path.dirname(__file__), 'fixtures/docopt_extractor')

        f = open(os.path.join(lib_path, expected_docopt))
        buffer = f.read()
        f.close()

        doe = DocoptExtractor(lib_path)

        self.assertEqual(lib_path, doe.lib_path)

        self.assertIsNotNone(doe.docopt(file_under_test))
        self.assertEqual("".join(buffer), doe.docopt(file_under_test))


if __name__ == '__main__':
    unittest.main()
