import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip_contact import Contact


class TestContact(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[samplecontact]", "expiration_time=zEXM15qvwidv1x", "outbound_proxy=e3BSr4", "path=TXGgYbS3CKmhXHeF5g", "qualify_frequency=l8jr", "type=oHFtT70hnBUQHCPv", "uri=SMsL9NehmsO", "user_agent=vTUxj9"], {"expiration_time":"zEXM15qvwidv1x", "outbound_proxy":"e3BSr4", "path":"TXGgYbS3CKmhXHeF5g", "qualify_frequency":"l8jr", "type":"oHFtT70hnBUQHCPv", "uri":"SMsL9NehmsO", "user_agent":"vTUxj9"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        contact = Contact(section)
        self.assertEqual(section, contact.section)

        contact.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(contact, attribute)
            self.assertEqual(expected_value, actual_value, "auth.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))


if __name__ == '__main__':
    unittest.main()
