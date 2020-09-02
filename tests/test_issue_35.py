import unittest
import os

from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision_factory import ProvisionFactory


class TestIssue35(unittest.TestCase):

    def issue_base(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_31")

if __name__ == '__main__':
    unittest.main()
