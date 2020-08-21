import unittest
import sys
import io
import re

from poly_py_tools.versionator import Versionator


class TestVersionator(unittest.TestCase):
    def test_version(self):

        pattern = r"v([0-9]{1,}\.){2}([0-9]{1,}-){2}[0-9a-z]{8}"
        version = Versionator.version()
        self.assertIsNotNone(re.match(pattern, version), "Regular expression check for the version failed. Got this: {}".format(version))

        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        Versionator.show_version()
        output = out.getvalue()

        self.assertEqual("polypy version: {}\n".format(version), output)


if __name__ == '__main__':
    unittest.main()
