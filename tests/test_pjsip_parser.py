import unittest
import os
from unittest_data_provider import data_provider
from poly_py_tools.pjsip_section_parser import PjSipSectionParser

class TestPjSipSectionParser(unittest.TestCase):

    def get_conf(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/pjsip/pjsip.conf")

    def test_init(self):
        section_parser = PjSipSectionParser(self.get_conf())
        self.assertEqual(self.get_conf(), section_parser.conf_file)

    provider_test_sanitize_line = lambda : (
        #line                                          expected_resultant_line
        ("permit=209.16.236.0     ;This is a fake IP.", "permit=209.16.236.0"),
    )

    @data_provider(provider_test_sanitize_line)
    def test_sanitize_line(self, line, expectant_resultant_line):
        section_parser = PjSipSectionParser(None)
        self.assertEqual(expectant_resultant_line, section_parser.sanitize_line(line))

    def test_parse_sections(self):

        section_parser = PjSipSectionParser(self.get_conf())
        section_parser.parse()
        self.assertEqual(18, len(section_parser.sections))

        for section in section_parser.sections:
            for line in section:
                self.assertGreater(len(line), 0)
                self.assertFalse(";" in line, "Line failed: {}".format(line))

    provider_section_meta = lambda : (
        (0, 8, "[6001]"),
        (1, 10, "[6002]"),
        (2, 4, "[simpletrans]"),
        (3, 9, "[tlstrans]"),
        (4, 5, "[auth6001]"),
        (5, 5, "[auth6002]"),
        (6, 3, "[6001]"),
        (7, 3, "[6002]"),
        (8, 12, "[bandwidth_cloud]"),
        (9, 5, "[bandwidth_cloud]"),
        (10, 5, "[bandwidth_cloud]"),
        (11, 5, "[bandwidth_cloud]"),
        (12, 3, "[example2.com]"),
        (13, 3, "[confacl]"),
        (14, 5, "[selfacl]"),
        (15, 5, "[contactacl]"),
        (16, 4, "[6001]"),
        (17, 4, "[6002]"),
    )

    @data_provider(provider_section_meta)
    def test_parse_sections_complete(self, section_number, expected_lines, expected_name):
        section_parser = PjSipSectionParser(self.get_conf())
        section_parser.parse()

        section = section_parser.sections[section_number]
        self.assertEqual(expected_name, section[0], "Section {} should have {} as the section name, but found {} instead.". format(section_number, expected_name, section[0]))
        self.assertEqual(expected_lines, len(section), "Section {} with name {} has {} lines and should have {}".format(section_number, section[0], len(section), expected_lines))


if __name__ == '__main__':
    unittest.main()
