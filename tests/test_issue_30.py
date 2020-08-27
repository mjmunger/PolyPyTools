import unittest
import os

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision_factory import ProvisionFactory

class TestIssue30(unittest.TestCase):
    def test_issue_30(self):
        self.skipTest()
        args = {'--force': False,
                 '-d': True,
                 '-v': 0,
                 '<csvfile>': [],
                 '<macaddress>': '0004f23a43bf',
                 'directory': False,
                 'endpoints': False,
                 'for': False,
                 'list': False,
                 'polycom': True,
                 'provision': True,
                 'using': False}

        fixture_directory = os.path.join(os.path.dirname(__file__), "fixtures/provision_polycom")

        pconf = PolypyConfig()
        pconf.add_search_path(fixture_directory)
        pconf.load()

        pconf.json['paths']['asterisk'] = fixture_directory

        args['config'] = pconf
        args['<args>'] = args

        factory = ProvisionFactory()
        runner = factory.get_runner(args)
        runner.run()



if __name__ == '__main__':
    unittest.main()
