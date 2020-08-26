import unittest

from poly_py_tools.pjsip.pjsip_factory import PJSipFactory
from poly_py_tools.pjsip.pjsip_generator import PJSipGenerator


class TestIssue28(unittest.TestCase):
    def test_issue_28(self):

        args = {'--force': False,
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
                 'with': False}

        factory = PJSipFactory()
        runner = factory.get_runner(args)



if __name__ == '__main__':
    unittest.main()
