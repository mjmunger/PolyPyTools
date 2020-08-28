import unittest
import os.path
import json
import copy
import site
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory

from unittest_data_provider import data_provider

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.column_mapper import ColumnMapper

from unittest.mock import patch, mock_open, Mock, MagicMock


class HelperTestValidate:
    states = None
    polycom_paths = ['000000000000.cfg', '000000000000-directory~.xml', "Config/applications.cfg", "Config/device.cfg",
                     "Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd", "Config/reg-advanced.cfg",
                     "Config/reg-basic.cfg", "Config/region.cfg", "Config/sip-basic.cfg", "Config/sip-interop.cfg",
                     "Config/site.cfg", "Config/video.cfg", "Config/video-integration.cfg"]

    def __init__(self, mock_states):
        # setup default states - everything exists
        default_states = {}
        default_states["/etc/asterisk/sip.conf"] = True
        default_states["/srv/tftp/Config"] = True
        for path in self.polycom_paths:
            default_states[os.path.join("/srv/tftp", path)] = True

        self.states = {**default_states, **mock_states}

    def lookup(self, path):
        return self.states[path]


class TestConfig(unittest.TestCase):
    provider_test_init = lambda: (
        (['000000000000.cfg', '000000000000-directory~.xml', "Config/applications.cfg", "Config/device.cfg",
          "Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd", "Config/reg-advanced.cfg",
          "Config/reg-basic.cfg", "Config/region.cfg", "Config/sip-basic.cfg", "Config/sip-interop.cfg",
          "Config/site.cfg", "Config/video.cfg", "Config/video-integration.cfg"],),
    )

    @data_provider(provider_test_init)
    def test_init(self, polycom_files):
        config = PolypyConfig()
        self.assertEqual(polycom_files, config.polycom_files)

    provider_test_find_config = lambda: (
        # check_paths                                    expected_config_path
        (["/path/to/current/directory", "/etc/polypy/"], "/path/to/current/directory/polypy.conf", True),
        (["/path/to/current/directory", "/etc/polypy/"], "/etc/polypy/polypy.conf", True),
        (["/path/to/current/directory", "/etc/polypy/"], None, False),
    )

    @data_provider(provider_test_find_config)
    def test_find_config(self, check_paths, expected_config_path, exists):

        with patch.object(os.path, "exists") as mock_os:
            mock_os.side_effect = lambda path: path == expected_config_path
            config = PolypyConfig()
            for path in check_paths:
                config.add_search_path(path)

            self.assertEqual(exists, config.find())
            self.assertEqual(expected_config_path, config.config_path)

    @staticmethod
    def create_config_tuples():
        fixtures_dir = os.path.join(os.path.dirname(__file__), 'fixtures/')
        base_config_path = os.path.join(fixtures_dir, "base_config.json")

        with open(base_config_path) as fp:
            base_config = json.load(fp)

        return_tuples = ()

        config1 = copy.deepcopy(base_config)
        config1['config_path'] = fixtures_dir
        config1['paths']['asterisk'] = os.path.join(fixtures_dir, "tests/fixtures/etc/asterisk/")
        config1['paths']['tftproot'] = os.path.join(fixtures_dir, "tests/fixtures/srv/tftp/")
        return_tuples = return_tuples + ((json.dumps(config1), ["/path/to/current/directory", "/etc/polypy/"],
                                          "/path/to/current/directory/polypy.conf",),)

        return return_tuples

    config_fixtures = lambda: TestConfig.create_config_tuples()

    @data_provider(config_fixtures)
    def test_load_config(self, config, check_paths, expected_config_path):

        with patch("os.path") as mock_os:
            with patch("builtins.open", mock_open(read_data=config)) as mock_file:
                mock_os.path.exists = lambda path: path == expected_config_path
                expected_config_object = json.loads(config)
                assert open(expected_config_path).read() == config
                mock_file.assert_called_with(expected_config_path)

                config = PolypyConfig()
                for path in check_paths:
                    config.add_search_path(path)
                config.find()
                config.load()
                self.assertEqual(expected_config_object, config.json)

    def test_add_search_path(self):
        config = PolypyConfig()
        config.add_search_path("/path/to/some/place")
        config.add_search_path("/etc/polypy")

        self.assertEqual(3, len(config.search_paths))

    @data_provider(config_fixtures)
    def test_write_config(self, config_string, check_paths, expected_config_path):
        config = PolypyConfig()
        config.json = json.loads(config_string)

        f = NamedTemporaryFile(delete=False)
        config.config_path = f.name
        config.write()

        with open(f.name, 'r') as written_config_fp:
            loaded_config = json.load(written_config_fp)
        self.assertEqual(json.loads(config_string), loaded_config)

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    @data_provider(config_fixtures)
    def test_write_config_failure(self, config_string, check_paths, expected_config_path):

        m = mock_open()
        with patch("builtins.open", m):
            config = PolypyConfig()
            config.config = json.loads(config_string)
            m.side_effect = PermissionError()
            with self.assertRaises(PermissionError):
                config.write()

    provider_test_write_default_config = lambda: (
        ({"lib_path": "/var/lib/polypy", "share_path": "/usr/share/polypy/", "config_path": "/etc/asterisk/polypy.conf",
          "package_path": "/usr/local/lib/python3.7/dist-packages/poly_py_tools", "server_addr": "127.0.0.1",
          "paths": {"asterisk": "/etc/asterisk/", "tftproot": "/srv/tftp/"},
          "dictionary": {"first": ["first", "firstname", "first name"], "last": ["last", "lastname", "last name"],
                         "exten": ["exten", "extension", "new extension"], "vm": ["vm", "voicemail"],
                         "mac": ["mac", "macaddr", "mac address", "physical address"], "email": ["email"],
                         "endpoint": ["device", "phone", "fax", "model"],
                         "cid_number": ["cid", "cname", "callerid", "Caller-ID"],
                         "priority": ["priority", "sort", "order by", "order"], "label": ["label"],
                         "did": ["contact", "direct phone", "did", "number"],
                         "group_dial": ["simul-ring", "group dial"], "site": ["site"]}, "csvmap": {}},),
    )

    @data_provider(provider_test_write_default_config)
    def test_write_default_config(self, expected_config):
        tmp_dir = TemporaryDirectory()
        tmp_config = os.path.join(tmp_dir.name, 'polypy.conf')
        config = PolypyConfig()
        config.write_default_config(tmp_config)

        with open(tmp_config) as fp:
            actual_config = json.load(fp)

        expected_config['config_path'] = tmp_config
        expected_config['package_path'] = os.path.join(site.getsitepackages()[0], "poly_py_tools")
        self.assertEqual(expected_config, actual_config)

        tmp_dir.cleanup()

    provider_test_set_path = lambda: (
        ("asterisk", "/current/working/directory/to/something", "/current/working/directory/to/something"),
        ("asterisk", "to/something", "/current/working/directory/to/something"),
        ("asterisk", ".", "/current/working/directory"),
        ("tftproot", "/current/working/directory/to/something", "/current/working/directory/to/something"),
        ("tftproot", "to/something", "/current/working/directory/to/something"),
        ("tftproot", ".", "/current/working/directory"),
    )

    @data_provider(provider_test_set_path)
    def test_set_path(self, path, target_path, expected_path):
        configs = {}
        configs['paths'] = {}
        configs['paths']['asterisk'] = ""
        configs['paths']['tftproot'] = ""

        f = NamedTemporaryFile(delete=False)

        with patch.object(os, 'getcwd', return_value="/current/working/directory") as mock_os:
            config = PolypyConfig()
            config.config_path = f.name
            config.json = configs
            config.set_path(path, target_path)

            self.assertEqual(expected_path, config.json['paths'][path])

            os.unlink(f.name)
            self.assertFalse(os.path.exists(f.name))

    def test_set_server(self):
        configs = {}
        configs['server_addr'] = ""
        f = NamedTemporaryFile(delete=False)

        config = PolypyConfig()
        config.json = configs
        config.config_path = f.name
        config.set_server("test.example.org")

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

        self.assertEqual("test.example.org", config.json['server_addr'])

    provider_test_validate = lambda: (
        # sip.conf exists    tftproot exists       missing_file_count  missing_polycom_files
        (True, True, 0, []),
        (False, True, 1, []),
        (True, False, 1, []),
        (True, True, 1, ["Config/features.cfg"]),
        (True, True, 4,
         ["Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd", "Config/reg-advanced.cfg"]),
        (False, True, 5,
         ["Config/features.cfg", "Config/H323.cfg", "Config/polycomConfig.xsd", "Config/reg-advanced.cfg"]),
    )

    @data_provider(provider_test_validate)
    def test_validate(self, sip_conf_state, tftproot_state, missing_file_count, missing_polycom_files):

        mock_states = {}
        mock_states["/etc/asterisk/sip.conf"] = sip_conf_state
        mock_states["/srv/tftp/"] = tftproot_state

        for path in missing_polycom_files:
            mock_states[os.path.join("/srv/tftp/", path)] = False

        helper = HelperTestValidate(mock_states)

        with patch("os.path.exists", MagicMock(side_effect=helper.lookup)) as mock_os_path:
            config = PolypyConfig()
            config.json = {"lib_path": "/var/lib/polypy", "share_path": "/usr/share/polypy/",
                             "config_path": "/tmp/polypy.conf",
                             "package_path": "/usr/local/lib/python3.7/dist-packages/poly_py_tools",
                             "server_addr": "127.0.0.1",
                             "paths": {"asterisk": "/etc/asterisk/", "tftproot": "/srv/tftp/"}}
            status = config.validate()

            failed_counter = 0
            for path in status:
                if status[path] is False:
                    failed_counter = failed_counter + 1

            self.assertEqual(missing_file_count, failed_counter)
            self.assertEqual(status['/etc/asterisk/'], sip_conf_state)
            self.assertEqual(status['/srv/tftp/'], tftproot_state)
            self.assertEqual(status["/srv/tftp/000000000000.cfg"], "000000000000.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/000000000000-directory~.xml"],
                             "000000000000-directory~.xml" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/applications.cfg"],
                             "Config/applications.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/device.cfg"], "Config/device.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/features.cfg"],
                             "Config/features.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/H323.cfg"], "Config/H323.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/polycomConfig.xsd"],
                             "Config/polycomConfig.xsd" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/reg-advanced.cfg"],
                             "Config/reg-advanced.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/reg-basic.cfg"],
                             "Config/reg-basic.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/region.cfg"], "Config/region.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/sip-basic.cfg"],
                             "Config/sip-basic.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/sip-interop.cfg"],
                             "Config/sip-interop.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/site.cfg"], "Config/site.cfg" not in missing_polycom_files)
            self.assertEqual(status["/srv/tftp/Config/video.cfg"], "Config/video.cfg" not in missing_polycom_files)

    provider_test_dictionary_add = lambda : (
        ("first", "nKhI"),
        ("last", "rAQhbM"),
        ("exten", "XZmx"),
        ("vm", "wOVLrkhDhWvisNXW"),
        ("mac", "oMbMxdFqBLWDfpDYl"),
        ("email", "FQSOXqCWP"),
        ("endpoint", "wPMRgSHhyXy"),
        ("cid_number", "ZqUaVz"),
        ("priority", "ckoJofRYAJ"),
        ("label", "vUkTydmDk"),
        ("did", "CQriEvEnQhbEIn"),
        ("group_dial", "nxFjCJshs"),
        ("site", "FnnBp"),
    )

    @data_provider(provider_test_dictionary_add)
    def test_dictionary_add(self, word, alias):
        f = NamedTemporaryFile(delete=False)
        config = PolypyConfig()
        config.config_path = f.name
        config.write_default_config(f.name)
        config.add_dictionary_alias(word, alias)

        self.assertTrue(alias in config.json['dictionary'][word])

        fp = open(f.name, 'r')
        resultant_config = json.load(fp)
        fp.close()

        self.assertTrue(alias in resultant_config['dictionary'][word])

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    @data_provider(provider_test_dictionary_add)
    def test_dictionary_del(self, word, alias):
        f = NamedTemporaryFile(delete=False)
        config = PolypyConfig()
        config.config_path = f.name
        config.write_default_config(f.name)
        config.add_dictionary_alias(word, alias)

        self.assertTrue(alias in config.json['dictionary'][word])

        fp = open(f.name, 'r')
        resultant_config = json.load(fp)
        fp.close()

        self.assertTrue(alias in resultant_config['dictionary'][word])

        config.del_dictionary_word(word, alias)

        self.assertFalse(alias in config.json['dictionary'][word])

        fp = open(f.name, 'r')
        resultant_config = json.load(fp)
        fp.close()

        self.assertFalse(alias in resultant_config['dictionary'][word])

        os.unlink(f.name)
        self.assertFalse(os.path.exists(f.name))

    provider_column_headers = lambda: (
        (["Last name", "First Name", "Title", "Extension ", "Voicemail ", "Direct Phone", "Simul-ring", "Device", "MAC", "Email", "site", "callerid", "label", "priority"], {"first": 1, "last": 0, "exten": 3, "vm": 4, "mac": 8, "email": 9, "endpoint": 7, "cid_number": 11, "priority": 13, "label": 12,  "did": 5, "group_dial": 6, "site": 10}),
    )

    @data_provider(provider_column_headers)
    def test_map_csv(self, header, expected_map):
        f = NamedTemporaryFile(delete=False)
        config = PolypyConfig()
        config.set_default_config(f.name)
        mapper = ColumnMapper(config)
        config.set_map(mapper.match_columns(header))

        fp = open(f.name, 'r')
        saved_configs = json.load(fp)
        fp.close()

        self.assertEqual(expected_map, saved_configs['csvmap'])

    def test_configs(self):
        config = PolypyConfig()
        config.json = "685d69b8-ff2d-40c4-85d9-08f4c453445b"
        self.assertEqual("685d69b8-ff2d-40c4-85d9-08f4c453445b", config.configs())

    def test_asterisk_path(self):
        config = PolypyConfig()
        config.json = {}
        config.json['paths'] = {}
        config.json['paths']['asterisk'] = "72de147f-f46c-4286-a443-b9b4d8abbf37"
        self.assertEqual("72de147f-f46c-4286-a443-b9b4d8abbf37", config.asterisk_path())

    def test_tftproot_path(self):
        config = PolypyConfig()
        config.json = {}
        config.json['paths'] = {}
        config.json['paths']['tftproot'] = "f3ab756c-a431-4c8f-92db-701906483121"
        self.assertEqual("f3ab756c-a431-4c8f-92db-701906483121", config.tftproot_path())

    def test_update_paths(self):
        config = PolypyConfig()
        config.json = {}
        config.json['paths'] = {}
        config.json['paths']['asterisk'] = "3253989b-a86e-415f-8f0f-99f0117c1f28"
        config.json['paths']['tftproot'] = "f646d882-8887-4639-a4b2-ca4930a4f4e2"

        self.assertEqual("3253989b-a86e-415f-8f0f-99f0117c1f28", config.asterisk_path())
        self.assertEqual("f646d882-8887-4639-a4b2-ca4930a4f4e2", config.tftproot_path())

        config.update_paths('asterisk', "1b9a1167-e01f-458c-a992-708dd71c2a4a")
        self.assertEqual("1b9a1167-e01f-458c-a992-708dd71c2a4a", config.asterisk_path())

        config.update_paths('tftproot', "f174c720-1aea-4feb-b949-79dc953d77f8")
        self.assertEqual("f174c720-1aea-4feb-b949-79dc953d77f8", config.tftproot_path())

    def test_pjsip_path(self):
        config = PolypyConfig()
        config.json = {}
        config.json['paths'] = {}
        config.json['paths']['asterisk'] = "a7707f61-2dd9-4653-8ea5-4cbad0402007"
        self.assertEqual("a7707f61-2dd9-4653-8ea5-4cbad0402007/pjsip.conf", config.pjsip_path())

        config.pjsip_path = MagicMock(return_value="aa7e7971-d515-49a4-8ded-38a04b0694d8")
        self.assertEqual("aa7e7971-d515-49a4-8ded-38a04b0694d8", config.pjsip_path())


if __name__ == '__main__':
    unittest.main()
