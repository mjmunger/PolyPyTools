import os

from poly_py_tools.site.nat_setup import NatSetup
from poly_py_tools.site.site_runner import SiteRunner
import xml.etree.ElementTree as ET

class DisableNat(SiteRunner):

    def disable_nat(self):
        """
        This is a facade for resetting NAT settings.
        Service this command: polypy [ options ] site setup voipprot for <site> --address=<address> [ --port=<port> ]
        :return:
        """

        self.container['<args>']['--ip'] = ""
        self.container['<args>']['--mediaPortStart'] = "0"
        self.container['<args>']['--signalPort'] = "0"
        self.container['<args>']['--keepalive'] = "0"

        nat_setup = NatSetup(self.container)
        nat_setup.run()

    def run(self):
        self.disable_nat()

        # print("NAT has been disabled for {}".format(self.container['<args>']['<site>']))
