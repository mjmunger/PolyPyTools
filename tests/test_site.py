import shutil
import sys
import unittest
import os
import io
from unittest.mock import MagicMock
import xml.etree.ElementTree as ET


from docopt import docopt
from unittest_data_provider import data_provider

from poly_py_tools.polypy_config import PolypyConfig
from poly_py_tools.provision.model_meta import ModelMeta
from poly_py_tools.site.site import Site


class TestSite(unittest.TestCase):

    @staticmethod
    def issue_tftproot():
        return os.path.join(TestSite.issue_root(), 'tftproot')

    def setUp(self) -> None:

        if not os.path.exists(TestSite.issue_tftproot()):
            os.mkdir(TestSite.issue_tftproot())

        siteroot = os.path.join(TestSite.issue_tftproot(), "org-example")
        if not os.path.exists(siteroot):
            os.mkdir(siteroot)

        config_src = os.path.join(TestSite.issue_root(), "6.3.0.14929/Config")

        for file in os.listdir(config_src):
            src = os.path.join(config_src, file)
            dst = os.path.join(siteroot, file)
            shutil.copy(src, dst)

    def tearDown(self) -> None:
        tftproot = os.path.join(TestSite.issue_root(), 'tftproot')
        if os.path.exists(tftproot):
            shutil.rmtree(tftproot)

    @staticmethod
    def issue_root():
        return os.path.join(os.path.dirname(__file__), 'fixtures/issue_35')

    provider_test_site = lambda : (
        ("polypy site init example.org", "Directory initialized: /Users/michael/py/PolyPyTools/tests/fixtures/issue_35/tftproot/org-example\n", "6.3.0.14929"),
        ("polypy site init example.org SPIP650", "Directory initialized: /Users/michael/py/PolyPyTools/tests/fixtures/issue_35/tftproot/org-example\n", "4.0.15.1009"),
    )
    @data_provider(provider_test_site)
    def test_site_init(self, command : str, expected_output : str , expected_firmware_version):

        argv = command.split(" ")
        sys.argv = argv

        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(TestSite.issue_root())
        pconf.find()
        pconf.load()
        pconf.json['paths']['tftproot'] = os.path.join(TestSite.issue_root(), 'tftproot')

        container['pconf'] = pconf

        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        # self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        # self.assertEqual(expected_output, output)
        siteroot = os.path.join(TestSite.issue_tftproot(), 'org-example')
        self.assertTrue(os.path.exists(siteroot))

        files = os.listdir(os.path.join(self.issue_root(), "{}/Config".format(expected_firmware_version)))

        for file in files:
            target_file = os.path.join(siteroot, file)
            self.assertTrue(os.path.exists(target_file), "{} should exist in the siteroot, but does not.".format(target_file))

        files = os.listdir(os.path.join(siteroot))

        for file in files:
            target_source_file = os.path.join(self.issue_root(), "{}/Config".format(expected_firmware_version))
            self.assertTrue(os.path.exists(target_source_file))

        sip_ver_file = os.path.join(siteroot, "sip.ver")
        self.assertTrue(os.path.exists(sip_ver_file))

        f = open(sip_ver_file, 'r')
        buffer = f.read()
        f.close()

        self.assertEqual("".join(buffer.strip()), expected_firmware_version)
    def setup_setup(self):
        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(TestSite.issue_root())
        pconf.find()
        pconf.load()
        pconf.json['paths']['tftproot'] = os.path.join(TestSite.issue_root(), 'tftproot')
        container['pconf'] = pconf
        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out
        # Setup the files that we need to flush.
        siteroot = os.path.join(pconf.json['paths']['tftproot'], "org-example")
        if not os.path.exists(siteroot):
            os.mkdir(siteroot)
        source_dir = os.path.join(TestSite.issue_root(), "4.0.15.1009/Config")
        src_cfg = os.path.join(source_dir, "site.cfg")
        dst_cfg = os.path.join(siteroot, "site.cfg")
        shutil.copy(src_cfg, dst_cfg)
        self.assertTrue(os.path.exists(dst_cfg))
        # End file setup.
        return container, out, pconf, siteroot
    provider_test_site_flush = lambda : (
        ("polypy site flush configs for example.org", "Configs flushed for /Users/michael/py/PolyPyTools/tests/fixtures/issue_35/tftproot/org-example\n", "4.0.15.1009"),
        ("polypy site flush configs for example.org", "Configs flushed for /Users/michael/py/PolyPyTools/tests/fixtures/issue_35/tftproot/org-example\n", "6.3.0.14929"),
    )

    @data_provider(provider_test_site_flush)
    def test_site_flush(self, command : str, expected_output : str, expected_firmware_version : str):

        argv = command.split(" ")
        sys.argv = argv

        # Container is reset in site.py. This is so we can mock things.
        container = {}
        pconf = PolypyConfig()
        pconf.add_search_path(TestSite.issue_root())
        pconf.find()
        pconf.load()
        pconf.json['paths']['tftproot'] = os.path.join(TestSite.issue_root(), 'tftproot')

        container['pconf'] = pconf

        saved_stdout = sys.stdout
        out = io.StringIO()
        sys.stdout = out

        #Setup the files that we need to flush.
        siteroot = os.path.join(pconf.json['paths']['tftproot'], "org-example")
        if not os.path.exists(siteroot):
            os.mkdir(siteroot)

        source_dir = os.path.join(TestSite.issue_root(), expected_firmware_version)
        source_config = os.path.join(source_dir, "Config")
        files = os.listdir(source_config)
        for file in files:
            src = os.path.join(source_config, file)
            dst = os.path.join(siteroot, file)
            shutil.copy(src, dst)

        src = os.path.join(source_dir, "sip.ver")
        dst = os.path.join(siteroot, "sip.ver")
        shutil.copy(src, dst)

        self.assertTrue(os.path.exists(dst))

        for file in files:
            target_file = os.path.exists(os.path.join(siteroot, file))
            self.assertTrue(target_file)

        # End file setup.

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        # self.assertEqual(expected_output, output)

        self.assertTrue(os.path.exists(siteroot))

        for file in files:
            target_file = os.path.join(siteroot, file)
            self.assertFalse(os.path.exists(target_file), "{} should not exist, but does.")

    provider_test_site_sntp = lambda : (
        ("polypy site setup sntp for example.org --offset=-18000", "-18000", "0.north-america.pool.ntp.org", "NTP Server for example.org set to -18000 using 0.north-america.pool.ntp.org\n"),
        ("polypy site setup sntp for example.org --offset=-24000 --server=some.ntp.server.org", "-24000", "some.ntp.server.org", "NTP Server for example.org set to -24000 using some.ntp.server.org\n"),
    )

    @data_provider(provider_test_site_sntp)
    def test_site_sntp(self, command, expected_offset, expected_server, expected_output):
        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        # self.assertEqual(expected_output, output)

        site_cfg = os.path.join(siteroot, "site.cfg")
        self.assertTrue(os.path.exists(site_cfg))
        tree = ET.parse(site_cfg)
        root = tree.getroot()
        node = root.find("device")
        node = node.find("device.sntp")
        self.assertEqual(node.attrib['device.sntp.gmtOffset'], expected_offset)
        self.assertEqual(node.attrib['device.sntp.serverName'], expected_server)

        set_node = node.find("device.sntp.gmtOffset")
        self.assertEqual(set_node.attrib['device.sntp.gmtOffset.set'], "1")

    provider_test_site_syslog = lambda : (
        ("polypy site setup syslog for example.org", "pbx.hph.io", "Syslog server set to pbx.hph.io for example.org.\n"),
        ("polypy site setup syslog for example.org --server=some.other.ntp.server", "some.other.ntp.server", "Syslog server set to some.other.ntp.server for example.org.\n"),
    )
    @data_provider(provider_test_site_syslog)
    def test_setup_syslog(self, command : str, expected_syslog_server, expected_output):
        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        self.assertEqual(expected_output, output)

        site_cfg = os.path.join(siteroot, "site.cfg")
        self.assertTrue(os.path.exists(site_cfg))
        tree = ET.parse(site_cfg)
        root = tree.getroot()
        node = root.find("device")
        node = node.find("device.syslog")
        self.assertEqual(node.attrib['device.syslog.prependMac'], "1")
        self.assertEqual(node.attrib['device.syslog.serverName'], expected_syslog_server)
        self.assertEqual(node.attrib['device.syslog.transport'], "UDP")

        tmp_node = node.find("device.syslog.prependMac")
        self.assertEqual("1", tmp_node.attrib['device.syslog.prependMac.set'])

        tmp_node = node.find("device.syslog.serverName")
        self.assertEqual("1", tmp_node.attrib['device.syslog.serverName.set'])

        tmp_node = node.find("device.syslog.transport")
        self.assertEqual("1", tmp_node.attrib['device.syslog.transport.set'])

    provider_test_setup_nat = lambda : (
        ("polypy site setup nat for example.org --keepalive=30", "30", "", "0", "0"),
        ("polypy site setup nat for example.org --keepalive=45 --ip=1.2.3.4", "45", "1.2.3.4", "0", "0"),
        ("polypy site setup nat for example.org --keepalive=60 --ip=1.2.3.4 --mediaPortStart=5061", "60", "1.2.3.4", "5061", "0"),
        ("polypy site setup nat for example.org --keepalive=15 --ip=1.2.3.4 --mediaPortStart=5061 --signalPort=1234", "15", "1.2.3.4", "5061", "1234"),
    )

    @data_provider(provider_test_setup_nat)
    def test_setup_nat(self, command : str, expected_keep_alive : str, expected_ip : str, expected_media_start_port : str, expected_signal_port : str):
        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()



        config_file = os.path.join(siteroot, "sip-interop.cfg")
        self.assertTrue(os.path.exists(config_file))
        tree = ET.parse(config_file)
        root = tree.getroot()
        node = root.find("nat")
        self.assertEqual(node.attrib['nat.ip'], expected_ip)
        self.assertEqual(node.attrib['nat.mediaPortStart'], expected_media_start_port)
        self.assertEqual(node.attrib['nat.signalPort'], expected_signal_port)

        tmp_node = node.find("nat.keepalive")
        self.assertEqual(expected_keep_alive, tmp_node.attrib['nat.keepalive.interval'])

        expected_output = "NAT configured for example.org.\n"
        self.assertEqual(expected_output, output)

    provider_test_setup_password = lambda : (
        ("polypy site setup password for example.org to 8675309", "8675309", "Phone password for example.org set to 8675309\n"),
    )

    @data_provider(provider_test_setup_password)
    def test_setup_password(self, command : str, expected_password : str, expected_output : str):
        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()



        config_file = os.path.join(siteroot, "site.cfg")
        self.assertTrue(os.path.exists(config_file))
        tree = ET.parse(config_file)
        root = tree.getroot()
        node = root.find("device")
        node = node.find("device.auth")
        self.assertEqual(node.attrib['device.auth.localAdminPassword'], expected_password)

        tmp_node = node.find("device.auth.localAdminPassword")
        self.assertEqual("1", tmp_node.attrib['device.auth.localAdminPassword.set'])

        self.assertEqual(expected_output, output)

    provider_test_add_digitmap = lambda : (
        ("polypy site setup digitmap for example.org add 1xx", "1xx", "3", "1xx added to digit map for example.org.\n"),
    )

    @data_provider(provider_test_add_digitmap)
    def test_add_digitmap(self, command: str, expected_digitmap: str, expected_timeouts: str, expected_output : str):
        """
        :param self:
        :param command: cli command
        :param expected_digitmap: should be the last element in the list.
        :param expected_timeouts: should also be the last element in the list.
        :return:
        """
        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        default_maps = "[2-9]11|0T|011xxx.T|[0-1][2-9]xxxxxxxxx|[2-9]xxxxxxxxx|[2-9]xxxT|**x.T".split("|")
        default_timeouts = "3|3|3|3|3|3|3".split("|")

        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()

        config_file = os.path.join(siteroot, "site.cfg")
        self.assertTrue(os.path.exists(config_file))
        tree = ET.parse(config_file)
        root = tree.getroot()
        dialplan_node = root.find("dialplan")

        digitmaps = dialplan_node.attrib['dialplan.digitmap'].split("|")
        self.assertEqual(digitmaps[len(digitmaps) -1], expected_digitmap)

        digitmap_node = dialplan_node.find("dialplan.digitmap")
        timeouts = digitmap_node.attrib['dialplan.digitmap.timeOut'].split("|")
        self.assertEqual(len(digitmaps), len(timeouts))
        self.assertEqual(expected_digitmap, digitmaps[len(digitmaps) -1])

        self.assertEqual(expected_output, output)

    provider_test_del_digitmap = lambda : (
        ("polypy site setup digitmap for example.org del [2-9]xxxxxxxxx", "[2-9]xxxxxxxxx", "[2-9]11|0T|011xxx.T|[0-1][2-9]xxxxxxxxx|[2-9]xxxT|**x.T", "[2-9]xxxxxxxxx removed from digit map for example.org.\n"),
    )

    @data_provider(provider_test_del_digitmap)
    def test_del_digitmap(self, command: str, expected_digitmap_not_present: str, expected_digitmap : str, expected_output : str):
        """
        :param self:
        :param command: cli command
        :param expected_digitmap: should be the last element in the list.
        :return:
        """
        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        default_maps = "[2-9]11|0T|011xxx.T|[0-1][2-9]xxxxxxxxx|[2-9]xxxxxxxxx|[2-9]xxxT|**x.T".split("|")
        default_timeouts = "3|3|3|3|3|3|3".split("|")

        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()

        config_file = os.path.join(siteroot, "site.cfg")
        self.assertTrue(os.path.exists(config_file))
        tree = ET.parse(config_file)
        root = tree.getroot()
        dialplan_node = root.find("dialplan")

        self.assertEqual(expected_digitmap, dialplan_node.attrib['dialplan.digitmap'])

        actual_digitmaps = dialplan_node.attrib['dialplan.digitmap'].split("|")
        expected_digitmap = expected_digitmap.split("|")

        self.assertEqual(len(expected_digitmap), len(actual_digitmaps))

        digitmap_node = dialplan_node.find("dialplan.digitmap")
        timeouts = digitmap_node.attrib['dialplan.digitmap.timeOut'].split("|")
        self.assertEqual(len(expected_digitmap), len(timeouts))

        self.assertEqual(expected_output, output)

    provider_setup_voipprot = lambda : (
        ("polypy site setup voipprot for example.org --address=192.168.250.1", "example.org", "192.168.250.1", "0", "Registration server for example.org has been set to 192.168.250.1.\n"),
        ("polypy site setup voipprot for example.org --address=192.168.250.1 --port=1234", "example.org", "192.168.250.1", "1234", "Registration server for example.org has been set to 192.168.250.1.\n"),
    )

    @data_provider(provider_setup_voipprot)
    def test_setup_voipprot(self, command: str, site: str, expected_address: str, expected_port : str, expected_output: str):
        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()

        config_file = os.path.join(siteroot, "sip-basic.cfg")
        self.assertTrue(os.path.exists(config_file))
        tree = ET.parse(config_file)
        root = tree.getroot()
        voipprot_node = root.find("voIpProt")
        server_node = voipprot_node.find("voIpProt.server")

        self.assertEqual(expected_address, server_node.attrib['voIpProt.server.1.address'])
        self.assertEqual(expected_port, server_node.attrib['voIpProt.server.1.port'])

        self.assertEqual(expected_output, output)

    provider_setup_vlan = lambda: (
        ("polypy site setup vlan for example.org enable",  "example.org", "fixed", "1", "1", "1", "VLAN for example.org has been enabled.\n" ),
        ("polypy site setup vlan for example.org disable", "example.org", "disabled", "0", "0", "0", "VLAN for example.org has been disabled.\n" ),
    )

    @data_provider(provider_setup_vlan)
    def test_setup_vlan(self, command: str,
                        site: str,
                        expected_state: str,
                        expected_lldpenabled: str,
                        expected_cdpenabled : str,
                        expected_set_value : str,
                        expected_output: str):

        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()

        config_file = os.path.join(siteroot, "site.cfg")
        self.assertTrue(os.path.exists(config_file))
        tree = ET.parse(config_file)
        root = tree.getroot()
        device_node = root.find("device")
        net_node = device_node.find("device.net")
        dhcp_node = device_node.find("device.dhcp")

        self.assertEqual(expected_state, dhcp_node.attrib['device.dhcp.dhcpVlanDiscUseOpt'])

        set_dhcp_vlan_disc_node = dhcp_node.find("device.dhcp.dhcpVlanDiscUseOpt")
        set_dhcp_vlan_disc_node.attrib['device.dhcp.dhcpVlanDiscUseOpt.set'] = expected_set_value

        self.assertEqual(net_node.attrib['lldpEnabled'], expected_lldpenabled)
        self.assertEqual(net_node.attrib['cdpEnabled'], expected_cdpenabled)

        set_nodes = [ 'lldpEnabled', 'cdpEnabled']
        for n in set_nodes:
            tmp_node = net_node.find("device.net.{}".format(n))
            tmp_node.attrib["device.net.{}.set".format(n)] = expected_set_value


        self.assertEqual(expected_output, output)

    provider_test_disable_nat = lambda: (
        ("polypy site disable nat for example.org", "example.org", "NAT configured for example.org.\n" ),
    )

    @data_provider(provider_test_disable_nat)
    def test_disable_nat(self, command: str,
                        site: str,
                        expected_output: str):

        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        sip_interop_cfg = os.path.join(TestSite.issue_tftproot(), "org-example/sip-interop.cfg")
        tree = ET.parse(sip_interop_cfg)
        root = tree.getroot()
        nat_node = root.find("nat")
        nat_node.attrib['nat.ip'] = "8.8.8.8"
        nat_node.attrib['nat.mediaPortStart'] = "10000"
        nat_node.attrib['nat.signalPort'] = "5060"

        keepalive_node = nat_node.find("nat.keepalive")
        keepalive_node.attrib['nat.keepalive.interval'] = "30"
        tree.write(sip_interop_cfg)

        tree = None


        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()

        self.assertTrue(os.path.exists(sip_interop_cfg))

        tree = ET.parse(sip_interop_cfg)
        root = tree.getroot()
        nat_node = root.find("nat")
        self.assertEqual("", nat_node.attrib['nat.ip'])
        self.assertEqual("0", nat_node.attrib['nat.mediaPortStart'])
        self.assertEqual("0", nat_node.attrib['nat.signalPort'])

        keepalive_node = nat_node.find("nat.keepalive")
        self.assertEqual(keepalive_node.attrib['nat.keepalive.interval'], "0")

        self.assertEqual(expected_output, output)

    provider_configure_presence = lambda: (
        ("polypy site enable presence for example.org", "example.org", "Presence enabled for example.org.\n", "1"),
        ("polypy site disable presence for example.org", "example.org", "Presence disabled for example.org.\n", "0"),
    )

    @data_provider(provider_configure_presence)
    def test_configure_presence(self, command: str,
                        site: str,
                        expected_output: str,
                        expected_presence_value):

        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        sip_features_cfg = os.path.join(TestSite.issue_tftproot(), "org-example/features.cfg")
        tree = ET.parse(sip_features_cfg)
        root = tree.getroot()
        feature_node = root.find("feature")
        presence_node = feature_node.find("feature.presence")

        self.assertEqual(expected_presence_value, presence_node.attrib['feature.presence.enabled'])

        self.assertEqual(expected_output, output)


    provider_configure_ptt = lambda: (
        ("polypy site enable ptt for example.org", "example.org", "Presence enabled for example.org.\n", "0", "1"),
        ("polypy site disable ptt for example.org", "example.org", "Presence disabled for example.org.\n", "0", "0"),
    )

    @data_provider(provider_configure_ptt)
    def test_configure_ptt(self, command: str,
                        site: str,
                        expected_output: str,
                        expected_callwaiting_value,
                        expected_mode_value):

        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        cfg_file = os.path.join(TestSite.issue_tftproot(), "org-example/site.cfg")
        tree = ET.parse(cfg_file)
        root = tree.getroot()
        ptt_node = root.find("ptt")

        ptt_call_waiting_node = ptt_node.find("ptt.callWaiting")
        self.assertEqual(expected_callwaiting_value, ptt_call_waiting_node.attrib["ptt.callWaiting.enable"])

        ptt_mode_node = ptt_node.find("ptt.pttMode")
        self.assertEqual(expected_mode_value, ptt_mode_node.attrib["ptt.pttMode.enable"])

        self.assertEqual(expected_output, output)

    provider_configure_pagemode = lambda: (
        ("polypy site enable paging for example.org --name=Page", "example.org", "Paging enabled for example.org.\n", "1", "Page"),
        ("polypy site disable paging for example.org", "example.org", "Paging disabled for example.org.\n", "0", ""),
    )

    @data_provider(provider_configure_pagemode)
    def test_configure_pagemode(self, command: str,
                        site: str,
                        expected_output: str,
                        expected_mode_value,
                        expected_name):

        argv = command.split(" ")
        sys.argv = argv

        container, out, pconf, siteroot = self.setup_setup()

        # Should match site.py's script. Mocking should go before here.
        import poly_py_tools.site.site
        args = docopt(poly_py_tools.site.site.__doc__)
        container['<args>'] = args
        container['meta'] = ModelMeta()
        container['meta'].get_firmware_base_dir = MagicMock(
            return_value=os.path.join(os.path.dirname(__file__), "fixtures/issue_35"))
        container['meta'].use_configs(pconf)

        site = Site(container)

        # Do assertions for setup prior to run here
        self.assertTrue(isinstance(site.pconf(), PolypyConfig))
        #  End pre-run assertions

        site.run()

        # Post run assertions
        output = out.getvalue()
        cfg_file = os.path.join(TestSite.issue_tftproot(), "org-example/site.cfg")
        tree = ET.parse(cfg_file)
        root = tree.getroot()
        ptt_node = root.find("ptt")

        ptt_pagemode = ptt_node.find("ptt.pageMode")
        self.assertEqual(expected_mode_value, ptt_pagemode.attrib["ptt.pageMode.enable"])

        if expected_mode_value == "1":
            self.assertEqual(expected_name, ptt_pagemode.attrib["ptt.pageMode.displayName"])


        self.assertEqual(expected_output, output)
if __name__ == '__main__':
    unittest.main()
