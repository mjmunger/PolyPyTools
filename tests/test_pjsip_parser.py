import unittest
import os
from unittest_data_provider import data_provider

from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig


class TestPjSipSectionParser(unittest.TestCase):

    def get_pconf(self):

        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), "fixtures/test_pjsip_parser/"))
        pconf.load()
        pconf.update_paths("asterisk", os.path.join(os.path.dirname(__file__), "fixtures/pjsip/"))
        return pconf

    def test_use(self):
        pconf = self.get_pconf()
        section_parser = PjSipSectionParser()
        section_parser.use_config(pconf)
        self.assertEqual(pconf, section_parser.pconf)

    def test_use_factory(self):
        factory = SipResourceFactory()
        section_parser = PjSipSectionParser()
        section_parser.use_factory(factory)
        self.assertEqual(factory, section_parser.factory)

    def test_use_factory(self):
        factory = SipResourceFactory()
        section_parser = PjSipSectionParser()
        section_parser.use_factory(factory)
        self.assertEqual(factory, section_parser.factory)

    def test_init(self):
        pconf = self.get_pconf()
        section_parser = PjSipSectionParser()
        section_parser.use_config(pconf)
        self.assertEqual(pconf, section_parser.pconf)

    provider_test_sanitize_line = lambda: (
        # line                                          expected_resultant_line
        ("permit=209.16.236.0     ;This is a fake IP.", "permit=209.16.236.0"),
    )

    @data_provider(provider_test_sanitize_line)
    def test_sanitize_line(self, line, expectant_resultant_line):
        section_parser = PjSipSectionParser()
        self.assertEqual(expectant_resultant_line, section_parser.sanitize_line(line))

    def test_parse_sections(self):

        factory = SipResourceFactory()
        section_parser = PjSipSectionParser()
        section_parser.use_config(self.get_pconf())
        section_parser.use_factory(factory)
        section_parser.parse()
        self.assertEqual(20, len(section_parser.sections))
        self.assertEqual(17, len(section_parser.resources))

        for section in section_parser.sections:
            for line in section:
                self.assertGreater(len(line), 0)
                self.assertFalse(";" in line, "Line failed: {}".format(line))

    provider_section_meta = lambda: (
        (0, 10, "[6001](some-site-template)"),
        (1, 10, "[6002]"),
        (2, 4, "[simpletrans]"),
        (3, 9, "[tlstrans]"),
        (4, 7, "[auth6001]"),
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
        (18, 7, "[auth6003]"),
        (19, 3, "[6003]"),
    )

    @data_provider(provider_section_meta)
    def test_parse_sections_complete(self, section_number, expected_lines, expected_name):
        factory = SipResourceFactory()
        section_parser = PjSipSectionParser()
        section_parser.use_config(self.get_pconf())
        section_parser.use_factory(factory)
        section_parser.parse()

        section = section_parser.sections[section_number]
        self.assertEqual(expected_name, section[0],
                         "Section {} should have {} as the section name, but found {} instead.".format(section_number,
                                                                                                       expected_name,
                                                                                                       section[0]))
        self.assertEqual(expected_lines, len(section),
                         "Section {} with name {} has {} lines and should have {}".format(section_number, section[0],
                                                                                          len(section), expected_lines))

    def test_use_proxy(self):
        target_mac = "0004f23a43bf"

        factory = SipResourceFactory()
        section_parser = PjSipSectionParser()
        section_parser.use_config(self.get_pconf())
        section_parser.use_factory(factory)
        section_parser.parse()
        endpoint = section_parser.get_endpoint(target_mac)
        endpoint.use_proxy("pbx.hph.io")
        self.assertEqual("pbx.hph.io", endpoint.sip_proxy)

    provider_test_get_endpoint = lambda : (
        ("0004f23a43bf", "0004f23a43bf"),
        ("0004F23A43BF", "0004f23a43bf"),
        ("00:04:F2:3A:43:BF", "0004f23a43bf"),
        ("00-04-F2-3A-43-BF", "0004f23a43bf"),
    )
    @data_provider(provider_test_get_endpoint)
    def test_get_endpoint(self, target_mac, expected_mac):

        factory = SipResourceFactory()
        section_parser = PjSipSectionParser()
        section_parser.use_config(self.get_pconf())
        section_parser.use_factory(factory)
        section_parser.parse()
        endpoint = section_parser.get_endpoint(target_mac)

        self.assertIsInstance(endpoint, Endpoint)
        self.assertEqual(expected_mac, endpoint.mac)

    def test_get_templates(self):
        factory = SipResourceFactory()
        pconf = self.get_pconf()
        pconf.update_paths("asterisk", os.path.join(os.path.dirname(__file__), "fixtures/issue_30/"))
        section_parser = PjSipSectionParser()
        section_parser.use_config(pconf)
        section_parser.use_factory(factory)
        section_parser.parse()

        self.assertEqual(3, len(section_parser.get_templates()))

    def test_get_endpoints_for_mac(self):
        factory = SipResourceFactory()
        pconf = self.get_pconf()
        pconf.update_paths("asterisk", os.path.join(os.path.dirname(__file__), "fixtures/issue_36/asterisk"))
        section_parser = PjSipSectionParser()
        section_parser.use_config(pconf)
        section_parser.use_factory(factory)
        section_parser.parse()

        endpoints = section_parser.get_endpoints_for_mac('0004f2e62aa4')
        self.assertEqual(2, len(endpoints))

        ep111 = endpoints.pop(0)
        ep104 = endpoints.pop(0)
        self.assertEqual('0004f2e62aa4111', ep111.section_name)
        self.assertEqual('0004f2e62aa4104', ep104.section_name)

if __name__ == '__main__':
    unittest.main()
