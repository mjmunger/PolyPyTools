import os

from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class SyslogSetup(SiteRunner):

    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def setup_syslog(self):
        """
        Service this command: polypy [ options ] site setup sntp for <site> --offset=<gmtoffset> [--server=<ntp_server> ]
        :return:
        """

        if self.container['<args>']['--server'] is None:
            self.container['<args>']['--server'] = "pbx.hph.io"

        tree = ET.parse(self.site_cfg())
        root = tree.getroot()
        node = root.find("device")
        node = node.find("device.syslog")
        node.attrib['device.syslog.prependMac'] = "1"
        node.attrib['device.syslog.transport'] = "UDP"
        node.attrib['device.syslog.serverName'] = self.container['<args>']['--server']

        sets = ["prependMac", "transport", "serverName"]
        for set in sets:
            tmp = node.find("device.syslog.{}".format(set))
            tmp.attrib["device.syslog.{}.set".format(set)] = "1"

        tree.write(self.site_cfg())

    def run(self):
        self.setup_syslog()
        print("Syslog Server for {} set to {}".format(self.container['<args>']['<site>'], self.container['<args>']['--server'] ))
