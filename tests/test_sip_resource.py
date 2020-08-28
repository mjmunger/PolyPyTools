import unittest
from unittest_data_provider import data_provider
from poly_py_tools.pjsip.resource import SipResource


class TestSipResource(unittest.TestCase):

    provider_test_init = lambda : (
        (["[1234]", "attr1=value1", "attr2=value2", "type=typevalue"], {"attr1":"value1", "attr2":"value2", "type": "typevalue"}, "1234"),
    )

    provider_fail_test_init = lambda : (
        (["[1234]", "attr1=value1", "attr3=value3"], {"attr1":"value1", "attr3":"val3e2"}),
    )

    @data_provider(provider_test_init)
    def test_init(self, section, expected_attributes, expected_section_name):
        resource = SipResource(section)
        self.assertEqual(section, resource.section)

    @data_provider(provider_test_init)
    def test_set_attributes(self, section, expected_attributes, expected_section_name):
        resource = SipResource(section)
        resource.set_attributes()

        self.assertEqual(resource.section_name, expected_section_name)
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
    def test_str(self, section, expected_attributes, expected_section_name):
        resource = SipResource(section)
        resource.set_attributes()
        expected_str = "section: ['[1234]', 'attr1=value1', 'attr2=value2', 'type=typevalue']\nsection_name: 1234\ntype: typevalue\nis_template: False\ndebug_mode: False\nverbosity: 0\nmessage: \nattr1: value1\nattr2: value2"
        self.assertEqual(expected_str, resource.__str__())

    @data_provider(provider_test_init)
    def test_parse_section(self, section, expected_attributes, expected_section_name):
        expected_section = section[0]
        resource = SipResource(section)
        resource.set_attributes()
        resource.section = expected_section

    def test_new_section(self):
        resource = SipResource("None")
        resource.new_section("6001")
        self.assertEqual("6001", resource.section_name)
        self.assertEqual("[6001]", resource.section)




if __name__ == '__main__':
    unittest.main()
