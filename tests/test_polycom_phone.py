import os
import shutil
import unittest
from unittest.mock import MagicMock
from xml.etree import ElementTree

from unittest_data_provider import data_provider

from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.provision.polycom_phone import PolycomPhone


class TestPolycomPhone(unittest.TestCase):
    def setUp(self) -> None:
        if not os.path.exists(self.issue_asterisk()):
            os.mkdir(self.issue_asterisk())

        if not os.path.exists(self.issue_tftproot()):
            os.mkdir(self.issue_tftproot())

    def tearDown(self) -> None:
        hitlist = []
        hitlist.append(self.issue_asterisk())
        hitlist.append(self.issue_tftproot())

        for dir in hitlist:
            if os.path.exists(dir):
                shutil.rmtree(dir)

    def issue_root(self):
        return os.path.join(os.path.dirname(__file__), 'fixtures/test_polycom_phone')

    def issue_asterisk(self):
        return os.path.join(self.issue_root(), 'asterisk')

    def issue_tftproot(self):
        return os.path.join(self.issue_root(), 'tftproot')


    def test_add_endpoints(self):
        ep1 = Endpoint(["[1234]", "model=SSIP7000", "mac=0004f23a43bf", "type=endpoint"])
        ep2 = Endpoint(["[5678]", "model=SSIP7000", "mac=0004f23a43b0", "type=endpoint"])

        ep1.set_attributes()
        ep2.set_attributes()

        phone = PolycomPhone()
        phone.add_endpoint(ep1)
        phone.add_endpoint(ep2)

        self.assertEqual(2, len(phone.endpoints))

    def test_remove_endpoint(self):
        ep1 = Endpoint(["[1234]", "model=SSIP7000", "mac=0004f23a43bf", "type=endpoint"])
        ep2 = Endpoint(["[5678]", "model=SSIP7000", "mac=0004f23a43b0", "type=endpoint"])

        ep1.set_attributes()
        ep2.set_attributes()

        phone = PolycomPhone()
        phone.add_endpoint(ep1)
        phone.add_endpoint(ep2)

        self.assertEqual(2, len(phone.endpoints))

        endpoint_name = "1234"
        phone.remove_endpoint(endpoint_name)

        self.assertEqual(1, len(phone.endpoints))

        key, ep = phone.endpoints.popitem()
        self.assertEqual("5678", ep.section_name)

    provider_test_has_mac = lambda : (
            ('0004f23a43bf', '0004f23a43bf'),
            ('00-04-f2-3a-43-bf', '0004f23a43bf'),
            ('00-04-F2-3A-43-BF', '0004f23a43bf'),
            ('00:04:f2:3a:43:bf', '0004f23a43bf'),
            ('00:04:F2:3A:43:BF', '0004f23a43bf'),
    )
    @data_provider(provider_test_has_mac)
    def test_has_mac(self, mac, expected_mac):
        phone = PolycomPhone()
        phone.has_mac(mac)
        self.assertEqual(expected_mac, phone.mac)

    def test_is_model(self):
        phone = PolycomPhone()
        phone.is_model("SPIP670")
        self.assertEqual("SPIP670", phone.model)

    def test_use_configs(self):
        phone = PolycomPhone()
        pconf = PolypyConfig()
        phone.use_configs(pconf)
        self.assertEqual(pconf, phone.pconf)

    def test_use_reference(self):
        phone = PolycomPhone()
        meta = ModelMeta()
        phone.use_model_meta(meta)
        self.assertEqual(meta, phone.model_meta)

    def test_bootstrap_cfg(self):

        factory = SipResourceFactory()

        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), 'fixtures/test_endpoint'))
        pconf.load()
        pconf.json['paths']['asterisk'] = os.path.join(os.path.dirname(__file__), "fixtures/pjsip/")
        pconf.set_path("tftproot", self.issue_tftproot())

        meta = ModelMeta()
        meta.get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))
        meta.use_configs(pconf)

        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(factory)
        parser.parse()

        target_mac = "0004f23a43bf"

        ep = parser.get_endpoint(target_mac)
        ep.set_attributes()
        ep.model = "SSIP7000"
        ep.load_aors(parser.resources)
        ep.load_auths(parser.resources)
        # ep.hydrate_registrations()

        phone = PolycomPhone()
        phone.use_configs(pconf)
        phone.is_model("SSIP7000")
        phone.has_mac("0004f23a43bf")
        phone.use_model_meta(meta)
        phone.is_located_at(ep.template)
        phone.write_bootstrap()

        expected_bootstrap_path = os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/4.0.15.1009/expected_bootstrap.cfg")
        f = open(expected_bootstrap_path, 'r')
        buffer = f.read()
        f.close()
        expected_bootstrap = "".join(buffer)

        src_firmware_path = "/tmp/firmware/4.0.15.1009/"

        if not os.path.exists(src_firmware_path):
            os.makedirs(src_firmware_path)

        src_bootstrap_cfg = os.path.join(src_firmware_path, "000000000000.cfg")

        if not os.path.exists(src_bootstrap_cfg):
            original_source = os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/4.0.15.1009/000000000000.cfg")
            shutil.copyfile(original_source, src_bootstrap_cfg)

        self.assertTrue(os.path.exists(src_bootstrap_cfg))
        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware/"))
        actual_bootstrap_cfg_xml = ElementTree.fromstring(phone.bootstrap_cfg(meta))
        target_node = "APPLICATION_SSIP7000"
        application_node = actual_bootstrap_cfg_xml.find(target_node)

        self.assertFalse(application_node is None)
        self.assertTrue(application_node.tag, "APPLICATION_SSIP7000")
        self.assertEqual("firmware/4.0.15.1009/3111-40000-001.sip.ld", application_node.attrib['APP_FILE_PATH_SSIP7000'])
        self.assertEqual("some-site-template/site.cfg, some-site-template/sip-interop.cfg, some-site-template/features.cfg, some-site-template/sip-basic.cfg, some-site-template/reg-advanced.cfg, some-site-template/0004f23a43bf", application_node.attrib['CONFIG_FILES_SSIP7000'])


    def test_basic_cfg(self):

        target_mac = "0004f2e62aa4"

        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), 'fixtures/issue_36'))
        pconf.load()
        # Use the asterisk pjsip.conf from issue_36!
        pconf.json['paths']['asterisk'] = os.path.join(os.path.dirname(__file__), "fixtures/issue_36/asterisk/")
        pconf.set_path("tftproot", self.issue_tftproot())

        factory = SipResourceFactory()
        meta = ModelMeta()
        meta.use_configs(pconf)

        meta.get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))

        parser = PjSipSectionParser()
        parser.use_config(pconf)
        parser.use_factory(factory)
        parser.parse()

        phone = PolycomPhone()
        phone.is_model("SPIP670")
        phone.has_mac(target_mac)
        phone.use_configs(pconf)
        phone.use_model_meta(meta)

        endpoints = parser.get_endpoints_for_mac(target_mac)
        for ep in endpoints:
            phone.add_endpoint(ep)

        phone.hydrate_registrations(parser.resources)

        phone.write_configs()

        expected_basic_cfg = os.path.join(os.path.dirname(__file__), 'fixtures/issue_36/expected/com-l-3-office/0004f2e62aa4')
        self.assertTrue(os.path.exists(expected_basic_cfg))

        expected_xml = ElementTree.ElementTree()
        expected_xml.parse(expected_basic_cfg)
        expected_root = expected_xml.getroot()
        expected_reg = expected_root.find("reg")

        actual_xml = ElementTree.ElementTree()
        actual_xml.parse(phone.config_target_file_path())
        actual_root = actual_xml.getroot()
        actual_reg = actual_root.find("reg")

        self.assertEqual(len(expected_reg.items()), len(actual_reg.items()))

        for i in range(1, 2):
            self.assertEqual(expected_reg.attrib["reg.{}.address".format(i)], actual_reg.attrib["reg.{}.address".format(i)])
            self.assertEqual(expected_reg.attrib["reg.{}.auth.password".format(i)], actual_reg.attrib["reg.{}.auth.password".format(i)])
            self.assertEqual(expected_reg.attrib["reg.{}.auth.userId".format(i)], actual_reg.attrib["reg.{}.auth.userId".format(i)])
            self.assertEqual(expected_reg.attrib["reg.{}.label".format(i)], actual_reg.attrib["reg.{}.label".format(i)])


    def test_basic_cfg_path(self):

        pconf = PolypyConfig()
        pconf.add_search_path(os.path.join(os.path.dirname(__file__), 'fixtures/test_endpoint'))
        pconf.load()
        # Use the asterisk pjsip.conf from issue_36!
        pconf.json['paths']['asterisk'] = os.path.join(os.path.dirname(__file__), "fixtures/issue_36/asterisk/")
        pconf.set_path("tftproot", self.issue_tftproot())

        factory = SipResourceFactory()
        meta = ModelMeta()
        meta.use_configs(pconf)

        meta.get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/fs/firmware"))

        phone = PolycomPhone()
        phone.is_model("SPIP670")
        phone.has_mac("0004f2e62aa4")
        phone.use_configs(pconf)
        phone.use_model_meta(meta)

        expected_firmware_path = os.path.join(meta.get_firmware_dir(phone.model), "Config/reg-basic.cfg")
        self.assertEqual(expected_firmware_path, phone.basic_cfg_path())

if __name__ == '__main__':
    unittest.main()
