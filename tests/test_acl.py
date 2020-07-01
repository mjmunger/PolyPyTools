import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip_acl import Acl


class TestAor(unittest.TestCase):

    provider_test_init = lambda :(
        #section                                                                                                                                                                                   expected_attributes
        (["[sampleacl]", "acl=edh4ugNone", "contact_acl=U0lNone", "contact_deny=3K4YGCaXqTUjjuNrIhWNone", "contact_permit=Yp8S7eNone", "deny=KPKYF09GVFib1zjCSNone", "permit=a5UNone"], {"acl":"edh4ugNone", "contact_acl":"U0lNone", "contact_deny":"3K4YGCaXqTUjjuNrIhWNone", "contact_permit":"Yp8S7eNone", "deny":"KPKYF09GVFib1zjCSNone", "permit":"a5UNone"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):

        acl = Acl(section)
        self.assertEqual(section, acl.section)

        acl.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(acl, attribute)
            self.assertEqual(expected_value, actual_value, "auth.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))


if __name__ == '__main__':
    unittest.main()
