import unittest
import os
from pprint import pprint
from xml.dom import minidom
# from xml.dom import Attr
from xml.dom.minidom import Element
from xml.dom.minidom import Attr

from unittest_data_provider import data_provider

from poly_py_tools.pjsip.aor import Aor
from poly_py_tools.pjsip.endpoint import Endpoint
from poly_py_tools.pjsip.resource_factory import SipResourceFactory
from poly_py_tools.pjsip.section_parser import PjSipSectionParser
from poly_py_tools.provision.polycom_config_writer import PolycomConfigWriter
from poly_py_tools.provision.model_meta import ModelMeta


class TestPolycomConfigWriter(unittest.TestCase):
    config_fixtures_unsupported = lambda : (
    )

    config_fixtures = lambda: (
        ('SPIP320', '3.3.5.0247', "firmware/3.3.5.0247/2345-12200-002.sip.ld", "APPLICATION_SPIP320",
         "APP_FILE_PATH_SPIP320", "CONFIG_FILES_SPIP320"),
        ('SPIP321', '4.0.15.1009', "firmware/4.0.15.1009/2345-12360-001.sip.ld", "APPLICATION_SPIP321",
         "APP_FILE_PATH_SPIP321", "CONFIG_FILES_SPIP321"),
        ('SPIP330', '3.3.5.0247', "firmware/3.3.5.0247/2345-12200-001.sip.ld", "APPLICATION_SPIP330",
         "APP_FILE_PATH_SPIP330", "CONFIG_FILES_SPIP330"),
        ('SSIP5000', '4.0.15.1009', "firmware/4.0.15.1009/3111-30900-001.sip.ld", "APPLICATION_SSIP5000",
         "APP_FILE_PATH_SSIP5000", "CONFIG_FILES_SSIP5000"),
        ('SPIP331', '4.0.15.1009', "firmware/4.0.15.1009/2345-12365-001.sip.ld", "APPLICATION_SPIP331",
         "APP_FILE_PATH_SPIP331", "CONFIG_FILES_SPIP331"),
        ('SPIP335', '4.0.15.1009', "firmware/4.0.15.1009/2345-12375-001.sip.ld", "APPLICATION_SPIP335",
         "APP_FILE_PATH_SPIP335", "CONFIG_FILES_SPIP335"),
        ('SSIP6000', '4.0.15.1009', "firmware/4.0.15.1009/3111-15600-001.sip.ld", "APPLICATION_SSIP6000",
         "APP_FILE_PATH_SSIP6000", "CONFIG_FILES_SSIP6000"),
        ('SPIP430', '3.2.7.0198', "firmware/3.2.7.0198/2345-11402-001.sip.ld", "APPLICATION_SPIP430",
         "APP_FILE_PATH_SPIP430", "CONFIG_FILES_SPIP430"),
        ('SPIP450', '4.0.15.1009', "firmware/4.0.15.1009/2345-12450-001.sip.ld", "APPLICATION_SPIP450",
         "APP_FILE_PATH_SPIP450", "CONFIG_FILES_SPIP450"),
        ('SPIP550', '4.0.15.1009', "firmware/4.0.15.1009/2345-12500-001.sip.ld", "APPLICATION_SPIP550",
         "APP_FILE_PATH_SPIP550", "CONFIG_FILES_SPIP550"),
        ('SPIP560', '4.0.15.1009', "firmware/4.0.15.1009/2345-12560-001.sip.ld", "APPLICATION_SPIP560",
         "APP_FILE_PATH_SPIP560", "CONFIG_FILES_SPIP560"),
        ('SPIP650', '4.0.15.1009', "firmware/4.0.15.1009/2345-12600-001.sip.ld", "APPLICATION_SPIP650",
         "APP_FILE_PATH_SPIP650", "CONFIG_FILES_SPIP650"),
        ('SPIP670', '4.0.15.1009', "firmware/4.0.15.1009/2345-12670-001.sip.ld", "APPLICATION_SPIP670",
         "APP_FILE_PATH_SPIP670", "CONFIG_FILES_SPIP670"),
        ('SSIP7000', '4.0.15.1009', "firmware/4.0.15.1009/3111-40000-001.sip.ld", "APPLICATION_SSIP7000",
         "APP_FILE_PATH_SSIP7000", "CONFIG_FILES_SSIP7000"),
        ('VVX101', '6.3.0.14929', "firmware/6.3.0.14929/3111-40250-001.sip.ld", "APPLICATION_VVX101",
         "APP_FILE_PATH_VVX101", "CONFIG_FILES_VVX101"),
        ('VVX150', '6.3.0.14929', "firmware/6.3.0.14929/3111-48810-001.sip.ld", "APPLICATION_VVX150",
         "APP_FILE_PATH_VVX150", "CONFIG_FILES_VVX150"),
        ('VVX1500', '5.9.6.2327', "firmware/5.9.6.2327/2345-17960-001.sip.ld", "APPLICATION_VVX1500",
         "APP_FILE_PATH_VVX1500", "CONFIG_FILES_VVX1500"),
        ('VVX201', '6.3.0.14929', "firmware/6.3.0.14929/3111-40450-001.sip.ld", "APPLICATION_VVX201",
         "APP_FILE_PATH_VVX201", "CONFIG_FILES_VVX201"),
        ('VVX250', '6.3.0.14929', "firmware/6.3.0.14929/3111-48820-001.sip.ld", "APPLICATION_VVX250",
         "APP_FILE_PATH_VVX250", "CONFIG_FILES_VVX250"),
        ('VVX300', '5.9.6.2327', "firmware/5.9.6.2327/3111-46135-002.sip.ld", "APPLICATION_VVX300",
         "APP_FILE_PATH_VVX300", "CONFIG_FILES_VVX300"),
        ('VVX301', '5.9.6.2327', "firmware/5.9.6.2327/3111-48300-001.sip.ld", "APPLICATION_VVX301",
         "APP_FILE_PATH_VVX301", "CONFIG_FILES_VVX301"),
        ('VVX310', '5.9.6.2327', "firmware/5.9.6.2327/3111-46161-001.sip.ld", "APPLICATION_VVX310",
         "APP_FILE_PATH_VVX310", "CONFIG_FILES_VVX310"),
        ('VVX311', '5.9.6.2327', "firmware/5.9.6.2327/3111-48350-001.sip.ld", "APPLICATION_VVX311",
         "APP_FILE_PATH_VVX311", "CONFIG_FILES_VVX311"),
        ('VVX350', '6.3.0.14929', "firmware/6.3.0.14929/3111-48830-001.sip.ld", "APPLICATION_VVX350",
         "APP_FILE_PATH_VVX350", "CONFIG_FILES_VVX350"),
        ('VVX400', '5.9.6.2327', "firmware/5.9.6.2327/3111-46157-002.sip.ld", "APPLICATION_VVX400",
         "APP_FILE_PATH_VVX400", "CONFIG_FILES_VVX400"),
        ('VVX401', '6.3.0.14929', "firmware/6.3.0.14929/3111-48400-001.sip.ld", "APPLICATION_VVX401",
         "APP_FILE_PATH_VVX401", "CONFIG_FILES_VVX401"),
        ('VVX410', '5.9.6.2327', "firmware/5.9.6.2327/3111-46162-001.sip.ld", "APPLICATION_VVX410",
         "APP_FILE_PATH_VVX410", "CONFIG_FILES_VVX410"),
        ('VVX411', '6.3.0.14929', "firmware/6.3.0.14929/3111-48450-001.sip.ld", "APPLICATION_VVX411",
         "APP_FILE_PATH_VVX411", "CONFIG_FILES_VVX411"),
        ('VVX450', '6.3.0.14929', "firmware/6.3.0.14929/3111-48840-001.sip.ld", "APPLICATION_VVX450",
         "APP_FILE_PATH_VVX450", "CONFIG_FILES_VVX450"),
        ('VVX500', '5.9.6.2327', "firmware/5.9.6.2327/3111-44500-001.sip.ld", "APPLICATION_VVX500",
         "APP_FILE_PATH_VVX500", "CONFIG_FILES_VVX500"),
        ('VVX501', '6.3.0.14929', "firmware/6.3.0.14929/3111-48500-001.sip.ld", "APPLICATION_VVX501",
         "APP_FILE_PATH_VVX501", "CONFIG_FILES_VVX501"),
        ('VVX600', '5.9.6.2327', "firmware/5.9.6.2327/3111-44600-001.sip.ld", "APPLICATION_VVX600",
         "APP_FILE_PATH_VVX600", "CONFIG_FILES_VVX600"),
        ('VVX601', '6.3.0.14929', "firmware/6.3.0.14929/3111-48600-001.sip.ld", "APPLICATION_VVX601",
         "APP_FILE_PATH_VVX601", "CONFIG_FILES_VVX601"),
        ('VVXD60', '6.3.0.14929', "firmware/6.3.0.14929/3111-17823-001.sip.ld", "APPLICATION_VVXD60",
         "APP_FILE_PATH_VVXD60", "CONFIG_FILES_VVXD60"),
    )

    def get_conf(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/pjsip/pjsip.conf")

    def test_set_debug_mode(self):
        writer = PolycomConfigWriter()
    
    provider_test_set_paths = lambda: (
        ({"lib_path": "/var/lib/polypy", "share_path": "/usr/share/polypy/",
         "config_path": "/root/clients/com.l-3.office/polypy.conf",
         "package_path": "/usr/local/lib/python3.7/site-packages/poly_py_tools",
         "paths": {"asterisk": "/root/clients/com.l-3.office/./asterisk/", "tftproot": "/var/www/html/io.hph.pbx/p/"},
         "server_addr": "pbx.hph.io",
         "dictionary": {"first": ["first", "firstname", "first name"], "last": ["last", "lastname", "last name"],
                        "exten": ["exten", "extension", "new extension"], "vm": ["vm", "voicemail"],
                        "mac": ["mac", "macaddr", "mac address", "physical address"], "email": ["email"],
                        "endpoint": ["device", "phone", "fax", "model"],
                        "cid_number": ["cid", "cname", "callerid", "Caller-ID"],
                        "priority": ["priority", "sort", "order by", "order"], "label": ["label"],
                        "did": ["contact", "direct phone", "did", "number"], "group_dial": ["simul-ring", "group dial"],
                        "site": ["site"]},
         "csvmap": {"first": 1, "last": 0, "exten": 3, "vm": 4, "mac": 8, "email": 9, "endpoint": 7, "cid_number": 11,
                    "priority": 13, "label": 12, "did": 5, "group_dial": 6, "site": 10}}, "/var/www/html/io.hph.pbx/p/",

         "/var/www/html/io.hph.pbx/p/firmware/4.0.15.1009",
         "/var/www/html/io.hph.pbx/p/firmware/4.0.15.1009/Config",
         "/var/www/html/io.hph.pbx/p/firmware/4.0.15.1009/Config/reg-basic.cfg",
         "/var/www/html/io.hph.pbx/p/8dc6ad8462be.cfg",
         "/var/www/html/io.hph.pbx/p/com-l-3-office",
         "/var/www/html/io.hph.pbx/p/com-l-3-office/8dc6ad8462be"),
    )

    @data_provider(provider_test_set_paths)
    def test_set_paths(self,
                       configs,
                       expected_tftproot,
                       expected_firmware_dir,
                       expected_config_dir,
                       expected_config_template,
                       expected_phone_boostrap_file,
                       expected_phone_config_dir,
                       expected_phone_config):
        model_meta = ModelMeta()

        device = Endpoint("[1234]")
        device.model = "SPIP670"
        device.mac = "8dc6ad8462be"
        device.template = "com-l-3-office"

        writer = PolycomConfigWriter()
        writer.load(model_meta)
        writer.use_configs(configs)
        writer.use(device)

        writer.set_path()
        self.assertEqual(expected_firmware_dir, writer.firmware_dir)
        self.assertEqual(expected_tftproot, writer.tftproot)
        self.assertEqual(expected_config_dir, writer.config_dir)
        self.assertEqual(expected_config_template, writer.config_template)
        self.assertEqual(expected_phone_boostrap_file, writer.phone_boostrap_file)
        self.assertEqual(expected_phone_config_dir, writer.phone_config_dir)
        self.assertEqual(expected_phone_config, writer.phone_config)

    def test_load(self):
        m = ModelMeta
        writer = PolycomConfigWriter()
        writer.load(m)
        self.assertEqual(m, writer.model_meta)

    def test_assemble_config_file_list(self):

        model_meta = ModelMeta()
        section = ["[1001] (some-template)", "type=endpoint", "mac=8dc6ad8462be", 'model=SPIP650']
        endpoint = Endpoint(section)
        endpoint.set_attributes()
        writer = PolycomConfigWriter()
        writer.load(model_meta)
        writer.use(endpoint)

        expected_file_list = "some-template/site.cfg, some-template/sip-interop.cfg, some-template/features.cfg, some-template/sip-basic.cfg, some-template/reg-advanced.cfg, some-template/8dc6ad8462be"

        self.assertEqual(expected_file_list, writer.assemble_config_file_list())

    @data_provider(config_fixtures)
    def test_get_cfg_application_element(self, model, expected_firmware_version, expected_firmware_path,
                                         expected_application_element, expected_file_path_attribute,
                                         expected_config_file_attribute):

        model_meta = ModelMeta()

        section = ["[1001] (some-template)", "type=endpoint", "mac=8dc6ad8462be", 'model={}'.format(model), '']
        endpoint = Endpoint(section)
        endpoint.set_attributes()
        aor1 = Aor("section1")
        aor2 = Aor("section2")

        endpoint.add_aor(aor1)
        endpoint.add_aor(aor2)

        writer = PolycomConfigWriter()
        # writer.use_configs(self.create_config_tuples())
        writer.load(model_meta)
        writer.use(endpoint)
        self.assertEqual(expected_application_element, writer.get_cfg_application_element())
        self.assertEqual(expected_file_path_attribute, writer.get_file_path_attribute())
        self.assertEqual(expected_config_file_attribute, writer.get_config_file_attribute())
        self.assertEqual(expected_firmware_path, writer.get_app_file_path())

    @data_provider(config_fixtures)
    def test_get_cfg(self, model, expected_firmware_version, expected_firmware_app, expected_application_element,
                     expected_file_path_attribute, expected_config_file_attribute):

        expected_file_list = "some-template/site.cfg, some-template/sip-interop.cfg, some-template/features.cfg, some-template/sip-basic.cfg, some-template/reg-advanced.cfg, some-template/8dc6ad8462be"
        model_meta = ModelMeta()

        section = ["[1001] (some-template)", "type=endpoint", "mac=8dc6ad8462be", 'model={}'.format(model), '']
        endpoint = Endpoint(section)
        endpoint.set_attributes()
        aor1 = Aor("section1")
        aor2 = Aor("section2")

        endpoint.add_aor(aor1)
        endpoint.add_aor(aor2)

        config = TestPolycomConfigWriter.provider_test_set_paths()[0][0]
        config['paths']['tftproot'] = os.path.join(os.path.dirname(__file__), "fixtures/fs/")

        writer = PolycomConfigWriter()
        writer.use_configs(config)
        writer.load(model_meta)
        writer.use(endpoint)
        writer.set_path()

        config_xml = writer.get_cfg()
        self.assertIsInstance(config_xml, minidom.Document)
        app = config_xml.getElementsByTagName(expected_application_element)[0]
        self.assertNotEqual(app, [], "Was looking for application element {}, but it does not exist, and it should.".format(expected_application_element))
        self.assertIsInstance(app, Element)

        actual_config_file_attribute = app.attributes[expected_config_file_attribute]

        self.assertIsInstance(actual_config_file_attribute, Attr)
        self.assertEqual(expected_file_list, actual_config_file_attribute.value)

        actual_app_file_path_attribute = app.attributes[expected_file_path_attribute]
        self.assertIsInstance(actual_app_file_path_attribute, Attr)
        self.assertEqual(expected_firmware_app, actual_app_file_path_attribute.value)

