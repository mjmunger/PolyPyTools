import unittest

from unittest_data_provider import data_provider

from poly_py_tools.site.digitmap_setup import DigitMapSetup
from poly_py_tools.site.nat_setup import NatSetup
from poly_py_tools.site.password_setup import PasswordSetup
from poly_py_tools.site.setup_vlan import SetupVlan
from poly_py_tools.site.setup_voipprot import SetupVoipProt
from poly_py_tools.site.site_configurator import SiteConfigurator
from poly_py_tools.site.site_factory import SiteFactory
from poly_py_tools.site.sntp_setup import SntpSetup
from poly_py_tools.site.syslog_setup import SyslogSetup


class TestSiteFactory(unittest.TestCase):
    provider_test_site_factory = lambda: (
        ({'<args>': {'site' :True, 'init': True, '<site>': 'example.org'}}, SiteConfigurator),
        ({'<args>': {'site' :True, 'flush': True, 'configs': True, 'for': True, '<site>': 'example.org'}}, SiteConfigurator),
        ({'<args>': {'site' :True, 'setup': True, 'setup': True, 'sntp': True, '<site>': 'example.org'}}, SntpSetup),
        ({'<args>': {'site' :True, 'setup': True, 'syslog': True, '<site>': 'example.org'}}, SyslogSetup),
        ({'<args>': {'site' :True, 'setup': True, 'nat': True, '<site>': 'example.org'}}, NatSetup),
        ({'<args>': {'site' :True, 'setup': True, 'password': True, '<site>': 'example.org'}}, PasswordSetup),
        ({'<args>': {'site' :True, 'setup': True, 'digitmap': True, '<site>': 'example.org'}}, DigitMapSetup),
        ({'<args>': {'site' :True, 'setup': True, 'voipprot': True, '<site>': 'example.org'}}, SetupVoipProt),
        ({'<args>': {'site' :True, 'setup': True, 'vlan': True, '<site>': 'example.org'}}, SetupVlan),
    )

    @data_provider(provider_test_site_factory)
    def test_site_factory(self, container, expected_class):
        factory = SiteFactory()
        obj = factory.create(container)
        self.assertTrue(isinstance(obj, expected_class))



if __name__ == '__main__':
    unittest.main()
