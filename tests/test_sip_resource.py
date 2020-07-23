import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip_resource import SipResource


class TestSipResource(unittest.TestCase):

    provider_test_init = lambda : (
        (["[1234]", "attr1=value1", "attr2=value2"], {"attr1":"value1", "attr2":"value2"}),
    )

    provider_fail_test_init = lambda : (
        (["[1234]", "attr1=value1", "attr3=value3"], {"attr1":"value1", "attr3":"val3e2"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes):
        resource = SipResource(section)
        self.assertEqual(section, resource.section)

    @data_provider(provider_test_init)
    def test_set_attributes(self, section, expected_attributes):
        resource = SipResource(section)
        resource.set_attributes()

        for attribute in expected_attributes:
            expected_value = expected_attributes[attribute]
            actual_value = getattr(resource, attribute)
            self.assertEqual(expected_value, actual_value, "resource.{} should be {}. Got {} instead.".format(attribute, expected_value, actual_value))

    @data_provider(provider_fail_test_init)
    def test_fail_missing_attribute(self, section, expected_attributes):
        resource = SipResource(section)
        with self.assertRaises(ValueError):
            resource.set_attributes()


    @data_provider(provider_test_init)
    def test_str(self, section, expected_attributes):
        resource = SipResource(section)
        resource.set_attributes()
        expected_str = "section: ['[1234]', 'attr1=value1', 'attr2=value2']\nattr1: value1\nattr2: value2"
        self.assertEqual(expected_str, resource.__str__())

    @data_provider(provider_test_init)
    def test_parse_section(self, section, expected_attributes):
        expected_section = section[0]
        resource = SipResource(section)
        resource.set_attributes()
        resource.section = expected_section




if __name__ == '__main__':
    unittest.main()
