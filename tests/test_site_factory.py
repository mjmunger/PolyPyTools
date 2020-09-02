import unittest

from unittest_data_provider import data_provider

from poly_py_tools.site.site_configurator import SiteConfigurator
from poly_py_tools.site.site_factory import SiteFactory


class TestSiteFactory(unittest.TestCase):
    provider_test_site_factory = lambda: (
        ({'<args>': {'site' :True, 'init': True, '<site>': 'example.org'}}, SiteConfigurator),
        ({'<args>': {'site' :True, 'flush': True, 'configs': True, 'for': True, '<site>': 'example.org'}}, SiteConfigurator),
    )

    @data_provider(provider_test_site_factory)
    def test_site_factory(self, container, expected_class):
        factory = SiteFactory()
        obj = factory.create(container)
        self.assertTrue(isinstance(obj, expected_class))



if __name__ == '__main__':
    unittest.main()
