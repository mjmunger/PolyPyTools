import xml
import xml.dom.minidom
import os


class SiteWriter:

    configs = None

    source_paths = {}
    dst_paths = {}
    site = None

    def __init__(self, configs):
        self.configs = configs
        print(configs)
        self.source_paths = {"device.cfg" : None, "features.cfg" : None, "H323.cfg" : None, "reg-advanced.cfg" : None,
                             "reg-basic.cfg" : None, "region.cfg": None, "sip-basic.cfg": None, "sip-interop.cfg": None,
                             "site.cfg" : None, "video.cfg" : None, "video-integration.cfg" : None}

        self.dst_paths = self.source_paths

    def setup_paths(self):
        print(self.configs['paths']['tftproot'])
        for k in self.source_paths:
            print(self.source_paths[k])
            self.source_paths[k] = os.path.join(os.path.join(self.configs['paths']['tftproot'], "Config"), k)

        for k in self.dst_paths:
            self.dst_paths[k] = os.path.join(self.configs['paths']['tftproot'], k)

    def set_site(self, site):
        self.site = site
        self.setup_paths()

    def setup_site_cfg(self):
        sitecfg = xml.dom.minidom.parse(self.source_paths['site.cfg'])
        root = sitecfg.getElementsByTagName('polycomConfig')

        #Enable syslog
        syslog_node = root[0].getElementsByTagName('device.syslog')
        syslog_node.setAttribute("device.syslog.prependMac", "1")
        syslog_node.setAttribute("device.syslog.serverName", "pbx.hph.io")
        syslog_node.setAttribute("device.syslog.transport", "UDP")

        root.toxml()

    def setup_all(self):

        self.setup_site_cfg()
        # self.enable_syslog()
        # self.setup_digit_map()
        # self.setup_ntp()

    def __str__(self):
        buffer = []
        buffer.append("Paths")
        buffer.append("  Source Paths")
        for k in self.source_paths:
            buffer.append("    {}: {}".format(k,self.source_paths[k]))

        buffer.append("  Dst Paths")
        for k in self.dst_paths:
            buffer.append("    {}: {}".format(k,self.dst_paths[k]))

        return "\n".join(buffer)
