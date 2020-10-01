import os

from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class SntpSetup(SiteRunner):

    def site_cfg(self):
        return os.path.join(self.siteroot(), "site.cfg")

    def setup_sntp(self):
        """
        Service this command: polypy [ options ] site setup sntp for <site> --offset=<gmtoffset> [--server=<ntp_server> ]
        :return:
        """

        # print(self.container['<args>'].keys())
        if "--server" not in self.container['<args>'].keys():
            self.container['<args>']['--server'] = "0.north-america.pool.ntp.org"

        if self.container['<args>']['--server'] is None:
            self.container['<args>']['--server'] = "0.north-america.pool.ntp.org"

        tree = ET.parse(self.site_cfg())
        root = tree.getroot()
        node = root.find("device")
        node.attrib['device.set'] = "1"

        node = node.find("device.sntp")
        node.attrib['device.sntp.gmtOffset'] = self.container['<args>']['--offset']
        node.attrib['device.sntp.serverName'] = self.container['<args>']['--server']

        set_node = node.find("device.sntp.gmtOffset")
        set_node.attrib['device.sntp.gmtOffset.set'] = "1"
        tree.write(self.site_cfg())

    def run(self):
        self.setup_sntp()
        print("NTP Server for {} set to {} using {}".format(self.container['<args>']['<site>'], self.container['<args>']['--offset'], self.container['<args>']['--server'] ))
