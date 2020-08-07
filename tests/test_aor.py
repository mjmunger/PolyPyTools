import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.aor import Aor


class TestAor(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[1234]", "contact=kFqQoCP3p0V7QNGZH0LNone", "default_expiration=s5eJt2Q3None", "mailboxes=YObnLxNone", "maximum_expiration=PBhNone", "max_contacts=rh6wsniO1ZDNone", "minimum_expiration=VljnodKNone", "remove_existing=XYn4oz4vV85None", "type=10QrSKsgNone", "qualify_frequency=iqZHoj3rEskmNone", "authenticate_qualify=UtZFSgt70None", "outbound_proxy=3JjeVpNOoGNone", "support_path=e7sDFP73None"], {"contact":"kFqQoCP3p0V7QNGZH0LNone", "default_expiration":"s5eJt2Q3None", "mailboxes":"YObnLxNone", "maximum_expiration":"PBhNone", "max_contacts":"rh6wsniO1ZDNone", "minimum_expiration":"VljnodKNone", "remove_existing":"XYn4oz4vV85None", "type":"10QrSKsgNone", "qualify_frequency":"iqZHoj3rEskmNone", "authenticate_qualify":"UtZFSgt70None", "outbound_proxy":"3JjeVpNOoGNone", "support_path":"e7sDFP73None"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        aor = Aor(section)
        self.assertEqual(section, aor.section)

        aor.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(aor, attribute)
            self.assertEqual(expected_value, actual_value, "aor.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))


if __name__ == '__main__':
    unittest.main()
