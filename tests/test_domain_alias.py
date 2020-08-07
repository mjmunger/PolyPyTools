import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.domain_alias import DomainAlias


class TestDomainAlias(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[sampledomain.com]", "type=E8Y78lp6NnRGxMxS19tc", "domain=qrUc8708Kp4Rryak"], {"type":"E8Y78lp6NnRGxMxS19tc", "domain":"qrUc8708Kp4Rryak"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        domain_alias = DomainAlias(section)
        self.assertEqual(section, domain_alias.section)

        domain_alias.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(domain_alias, attribute)
            self.assertEqual(expected_value, actual_value, "auth.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))


if __name__ == '__main__':
    unittest.main()
