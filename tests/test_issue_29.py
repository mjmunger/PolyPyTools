import unittest
import os

from pwgen_secure.rpg import Rpg

from poly_py_tools.pjsip.pjsip_factory import PJSipFactory
from poly_py_tools.polypy_config import PolypyConfig


class TestIssue29(unittest.TestCase):
    def test_issue_29(self):

        fixture_path = os.path.join(os.path.dirname(__file__), "fixtures/pjsip_generator")
        csv_path = os.path.join(fixture_path, 'DialPlanBuilder-ExampleOrg.csv')

        args = {'--force': False,
                 '-d': True,
                 '-v': 0,
                 '<column>': None,
                 '<extension>': '111',
                 '<file>': csv_path,
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

        pconf = PolypyConfig()
        pconf.add_search_path(fixture_path)
        pconf.load()

        args['config'] = pconf
        args['<args>'] = args
        args['rpg'] = Rpg("strong", None)

        factory = PJSipFactory()
        runner = factory.get_runner(args)
        runner.run()


if __name__ == '__main__':
    unittest.main()
