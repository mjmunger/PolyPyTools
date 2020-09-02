import os

from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class NatSetup(SiteRunner):

    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def sip_interop_config(self):
        return os.path.join(self.siteroot(), "sip-interop.cfg")

    def setup_nat(self):
        """
        Service this command: polypy [ options ] site setup sntp for <site> --offset=<gmtoffset> [--server=<ntp_server> ]
        :return:
        """

        tree = ET.parse(self.sip_interop_config())
        root = tree.getroot()
        node = root.find("nat")

        if self.container['<args>']['--ip'] is not None:
            node.attrib['nat.ip'] = self.container['<args>']['--ip']
        else:
            node.attrib['nat.ip'] = ""

        if self.container['<args>']['--mediaPortStart'] is not None:
            node.attrib['nat.mediaPortStart'] = self.container['<args>']['--mediaPortStart']
        else:
            node.attrib['nat.mediaPortStart'] = "0"

        if self.container['<args>']['--signalPort'] is not None:
            node.attrib['nat.signalPort'] = self.container['<args>']['--signalPort']
        else:
            node.attrib['nat.signalPort'] = "0"

        tmp = node.find("nat.keepalive")
        tmp.attrib['nat.keepalive.interval'] = self.container['<args>']['--keepalive']

        tree.write(self.sip_interop_config())

    def run(self):
        self.setup_nat()
        print("NAT configured for {}.".format(self.container['<args>']['<site>']))
