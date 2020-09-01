import xml
import xml.dom.minidom
import os
from shutil import copy


class SiteWriter:

    configs = None
    args = None

    source_paths = {}
    dst_paths = {}
    site = None
    gmtOffset = None
    debug_mode = False
    syslog_server = "pbx.hph.io"
    ntp_server = "0.north-america.pool.ntp.org"
    nat_ip = None
    nat_media_start_port = None
    nat_signal_port = None
    nat_interval = None

    def __init__(self, configs, args):
        self.args = args
        self.configs = configs

        self.source_paths = {"device.cfg" : None, "features.cfg" : None, "H323.cfg" : None, "reg-advanced.cfg" : None,
                             "reg-basic.cfg" : None, "region.cfg": None, "sip-basic.cfg": None, "sip-interop.cfg": None,
                             "site.cfg" : None, "video.cfg" : None, "video-integration.cfg" : None}

        self.dst_paths = self.source_paths.copy()

    def setup_paths(self):
        for k in self.source_paths:
            self.source_paths[k] = os.path.join(os.path.join(self.configs['paths']['tftproot'], "Config"), k)

        for k in self.dst_paths:
            self.dst_paths[k] = os.path.join(os.path.join(self.configs['paths']['tftproot'], self.site), k)

    def set_site(self, site):
        buffer = str(site).split(".")
        buffer.reverse()
        self.site = "-".join(buffer)
        self.setup_paths()

    def set_gmt_offset(self, gmtOffset):
        # self.gmtOffset = str(int(gmtOffset) * -1)
        self.gmtOffset = gmtOffset
        if self.debug_mode:
            print("gmtOffset set to: {}".format(self.gmtOffset))

    def get_cfg(self, file):
        return self.dst_paths[file] if os.path.exists(self.dst_paths[file]) else self.source_paths[file]

    def setup_site_cfg(self):
        root, syslog_node = self.setup_syslog()

        if self.debug_mode:
            print(syslog_node.toxml())

        sntp_node = self.setup_sntp(root)

        if self.debug_mode:
            print("SNTP:")
            print(sntp_node.toxml())

    def setup_syslog(self):

        sitecfg = xml.dom.minidom.parse(self.get_cfg('site.cfg'))
        root = sitecfg.getElementsByTagName('polycomConfig')[0]

        syslog_node = root.getElementsByTagName('device.syslog')[0]
        syslog_node.setAttribute("device.syslog.prependMac", "1")
        syslog_node.setAttribute("device.syslog.serverName", self.syslog_server)
        syslog_node.setAttribute("device.syslog.transport", "UDP")

        device_syslog_prependMac = syslog_node.getElementsByTagName("device.syslog.prependMac")[0]
        device_syslog_prependMac.setAttribute("device.syslog.prependMac.set", "1")

        device_syslog_serverName = syslog_node.getElementsByTagName("device.syslog.serverName")[0]
        device_syslog_serverName.setAttribute("device.syslog.serverName.set", "1")

        device_syslog_transport = syslog_node.getElementsByTagName("device.syslog.transport")[0]
        device_syslog_transport.setAttribute("device.syslog.transport.set", "1")

        self.save_cfg('site.cfg', sitecfg)

    def setup_sntp(self):

        sitecfg = xml.dom.minidom.parse(self.get_cfg('site.cfg'))
        root = sitecfg.getElementsByTagName('polycomConfig')[0]

        sntp_node = root.getElementsByTagName("device.sntp")[0]
        sntp_node.setAttribute("device.sntp.gmtOffset", self.gmtOffset)
        sntp_node.setAttribute("device.sntp.serverName", self.ntp_server)
        sntp_node_gmtoffset = sntp_node.getElementsByTagName("device.sntp.gmtOffset")[0]
        sntp_node_gmtoffset.setAttribute("device.sntp.gmtOffset.set", "1")
        sntp_node_server_name = sntp_node.getElementsByTagName("device.sntp.serverName")[0]
        sntp_node_server_name.setAttribute("device.sntp.serverName.set", "1")

        self.save_cfg('site.cfg', sitecfg)

    def save_cfg(self, cfg_file, xml_document):
        print("Saving: {}".format(self.dst_paths[cfg_file]))
        fp = open(self.dst_paths[cfg_file], 'w')
        fp.write(xml_document.toxml())
        fp.close()

    def setup_nat(self):

        sip_interop = xml.dom.minidom.parse(self.get_cfg('sip-interop.cfg'))
        root = sip_interop.getElementsByTagName('polycomConfig')[0]

        nat_node = root.getElementsByTagName("nat")[0]
        nat_node.setAttribute("nat.ip", self.nat_ip)
        nat_node.setAttribute("nat.mediaStartPort", self.nat_media_start_port)
        nat_node.setAttribute("nat.signalPort", self.nat_signal_port)
        nat_node.setAttribute("nat.keepalive.interval", self.nat_interval)

        self.save_cfg('sip-interop.cfg', sip_interop)

    def __str__(self):
        buffer = []
        buffer.append("Debug mode: {}".format("On" if self.debug_mode else "Off"))
        buffer.append("Paths")
        buffer.append("  Source Paths")
        for k in self.source_paths:
            buffer.append("    {}: {}".format(k,self.source_paths[k]))

        buffer.append("  Dst Paths")
        for k in self.dst_paths:
            buffer.append("    {}: {}".format(k,self.dst_paths[k]))

        return "\n".join(buffer)

    def setup_local_admin_password(self, password):
        site_cfg = xml.dom.minidom.parse(self.get_cfg('site.cfg'))
        root = site_cfg.getElementsByTagName('polycomConfig')[0]

        device_node = root.getElementsByTagName("device")[0]

        auth_node = device_node.getElementsByTagName("device.auth")[0]
        auth_node.setAttribute("device.auth.localAdminPassword", password)

        self.save_cfg("site.cfg", site_cfg)

    def del_digitmap(self, pattern):
        site_cfg = xml.dom.minidom.parse(self.get_cfg('site.cfg'))
        root = site_cfg.getElementsByTagName('polycomConfig')[0]

        dialplan_node = root.getElementsByTagName("dialplan")[0]
        digitmap = dialplan_node.getAttribute("dialplan.digitmap").split("|")
        digitmap.remove(pattern)
        dialplan_node.setAttribute("dialplan.digitmap", "|".join(digitmap))

        self.set_digitmap_timeouts(digitmap, root)

        self.save_cfg("site.cfg", site_cfg)

    def add_digitmap(self, pattern):
        site_cfg = xml.dom.minidom.parse(self.get_cfg('site.cfg'))
        root = site_cfg.getElementsByTagName('polycomConfig')[0]

        dialplan_node = root.getElementsByTagName("dialplan")[0]
        digitmap = dialplan_node.getAttribute("dialplan.digitmap").split("|")
        digitmap.append(pattern)
        dialplan_node.setAttribute("dialplan.digitmap", "|".join(digitmap))

        self.set_digitmap_timeouts(digitmap, root)

        self.save_cfg("site.cfg", site_cfg)

    def set_digitmap_timeouts(self, digitmap, root):
        timeouts = "|".join(["3"] * len(digitmap))
        digitmap_node = root.getElementsByTagName("dialplan.digitmap")[0]
        digitmap_node.setAttribute("dialplan.digitmap.timeOut", timeouts)

    def setup_voipprot(self, address, port):
        basic_cfg = xml.dom.minidom.parse(self.get_cfg('sip-basic.cfg'))
        root = basic_cfg.getElementsByTagName('polycomConfig')[0]

        prot_node = root.getElementsByTagName("voIpProt.server")[0]
        prot_node.setAttribute("voIpProt.server.1.address", address)
        prot_node.setAttribute("voIpProt.server.1.port", port)

        self.save_cfg("sip-basic.cfg", basic_cfg)

    def flush_cfgs(self):
        for cfg in self.dst_paths:
            print("Removing: {}".format(self.dst_paths[cfg]))
            os.remove(self.dst_paths[cfg])

        print("Done. Configs flushed.")

    def fill_cfgs(self):
        for cfg in self.dst_paths:
            if not os.path.exists(self.dst_paths[cfg]):
                copy(self.source_paths[cfg], self.dst_paths[cfg])
                print("Filling: {}".format(cfg))

    def disable_vlan(self):
        site_cfg = xml.dom.minidom.parse(self.get_cfg('site.cfg'))
        root = site_cfg.getElementsByTagName('polycomConfig')[0]

        device_node = root.getElementsByTagName("device")[0]

        auth_node = device_node.getElementsByTagName("device.net")[0]
        auth_node.setAttribute("lldpEnabled", "0")
        auth_node.setAttribute("cdpEnabled", "0")

        set_lldp_node = device_node.getElementsByTagName("device.net.lldpEnabled")[0]
        set_lldp_node.setAttribute("device.net.lldpEnabled.set", "1")

        set_cdp_node = device_node.getElementsByTagName("device.net.cdpEnabled")[0]
        set_cdp_node.setAttribute("device.net.cdpEnabled.set", "1")

        dhcp_node = root.getElementsByTagName("device.dhcp")[0]
        dhcp_node.setAttribute("device.dhcp.dhcpVlanDiscUseOpt", 'disabled')

        set_dhcp_vlan_disc_node = dhcp_node.getElementsByTagName("device.dhcp.dhcpVlanDiscUseOpt")[0]
        set_dhcp_vlan_disc_node.setAttribute("device.dhcp.dhcpVlanDiscUseOpt.set", "1")

        self.save_cfg("site.cfg", site_cfg)

    def enable_vlan(self):
        site_cfg = xml.dom.minidom.parse(self.get_cfg('site.cfg'))
        root = site_cfg.getElementsByTagName('polycomConfig')[0]

        device_node = root.getElementsByTagName("device")[0]

        dhcp_node = root.getElementsByTagName("device.dhcp")[0]
        dhcp_node.setAttribute("device.dhcp.dhcpVlanDiscUseOpt", 'fixed')

        set_dhcp_vlan_disc_node = dhcp_node.getElementsByTagName("device.dhcp.dhcpVlanDiscUseOpt")[0]
        set_dhcp_vlan_disc_node.setAttribute("device.dhcp.dhcpVlanDiscUseOpt.set", "0")

        auth_node = device_node.getElementsByTagName("device.net")[0]
        auth_node.setAttribute("lldpEnabled", "1")
        auth_node.setAttribute("cdpEnabled", "1")

        set_lldp_node = device_node.getElementsByTagName("device.net.lldpEnabled")[0]
        set_lldp_node.setAttribute("device.net.lldpEnabled.set", "1")

        set_cdp_node = device_node.getElementsByTagName("device.net.cdpEnabled")[0]
        set_cdp_node.setAttribute("device.net.cdpEnabled.set", "1")

        self.save_cfg("site.cfg", site_cfg)
