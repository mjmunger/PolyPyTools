import sys
import unittest
from docopt import docopt

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.site.site import Site


class TestSite(unittest.TestCase):
    def test_site(self):

        argv = "./polypy.py site setup syslog for example.org".split(" ")
        sys.argv = argv

        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        container['pconf'] = pconf
        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(PolypyConfig, site.pconf()))
        #  End pre-run assertions
        site.run()

        # Post run assertions



if __name__ == '__main__':
    unittest.main()
