import unittest
from unittest_data_provider import data_provider


class TestPjSipSection(unittest.TestCase):

    provider_test_init = lambda : (
        #section_name,  expected_section_name
        ("[6001]",      "6001")
    )

    def test_init(self, section_name, expected_section_name):
        endpoint = PjSipSection(section_name)
        self.assertEqual(endpoint.section_name, expected_section_name)


    def test_parse_sections(self):


if __name__ == '__main__':
    unittest.main()
