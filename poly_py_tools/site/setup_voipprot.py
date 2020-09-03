import os

from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class SetupVoipProt(SiteRunner):

    def setup_voipprot(self):
        """
        Service this command: polypy [ options ] site setup voipprot for <site> --address=<address> [ --port=<port> ]
        :return:
        """

        if self.container['<args>']['--port'] is None:
            self.container['<args>']['--port'] = "0"
        tree = ET.parse(self.basic_cfg())
        root = tree.getroot()
        node = root.find("voIpProt")
        node = node.find("voIpProt.server")
        node.attrib['voIpProt.server.1.address'] = self.container['<args>']['--address']
        node.attrib['voIpProt.server.1.port'] = self.container['<args>']['--port']

        tree.write(self.basic_cfg())

    def run(self):
        self.setup_voipprot()

        print("Registration server for {} has been set to {}.".format(self.container['<args>']['<site>'], self.container['<args>']['--address']))
